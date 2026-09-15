"""
Small, targeted monkeypatches applied on top of the installed doc2mark 0.6.1
package, addressing three specific bugs confirmed by direct inspection of
doc2mark's own source (.venv_doc2mark/lib/python3.11/site-packages/doc2mark/
pipelines/pymupdf_advanced_pipeline.py) during the TC28/TC29/TC30 fix pass.

Each patch wraps the ORIGINAL doc2mark method/function and delegates to it
first, so all of doc2mark's existing extraction/classification/table logic
is reused unchanged. Only the specific narrow behavior described below is
altered. Import this module (see run_doc2mark.py) before calling doc2mark;
it is applied once, at import time, via monkeypatching -- no files inside
the installed package are edited.

Fix 1 -- reading order across multi-column pages (TC28)
--------------------------------------------------------
`PDFLoader._process_page` sorts all content items on a page purely by
`position_y` (see pymupdf_advanced_pipeline.py:684:
`content_items.sort(key=lambda x: x.position_y)`), with no column/x
awareness at all -- confirmed by `doc2mark.core.types.SimpleContent` (the
per-item record) never storing an x-coordinate in the first place. On a
genuinely 2-column page this interleaves the two columns by raw vertical
position instead of reading column 1 fully then column 2, producing the
exact displaced-fragment corruption documented on TC28
(bulletin_no_212.pdf).

This patch re-derives each text block's x0 by re-reading the same
`page.get_text("dict")` structure doc2mark itself already parses (no new
extraction pass, no separate parser), and treats any block spanning >=62%
of the page width as a heading/footer that keeps its natural vertical
position relative to both columns. The remaining ("narrow") blocks are
only split into left/right columns when their x0 values show real evidence
of two distinct clusters -- a gap larger than 15% of the page width,
roughly centered on the page (25%-75%) -- which a genuinely single-column
page's short lines (headings, letterhead, list items) never produce, since
they all start at the same left margin as the page's long paragraphs
regardless of how short they are. An earlier version of this patch used
block width alone as a proxy for column membership and mis-split a
single-column fee schedule (schedule_of_analysis_charges_2026.pdf, TC31)
whose short heading lines happened to be narrower than its body paragraphs;
this was caught by re-running every TC27-TC31 fixture through the patch
before adopting it (see the regression check below) and fixed by requiring
the two-cluster gap evidence. Pages that don't show that evidence are left
completely unmodified -- the original position_y-only order is kept.

Fix 2 -- inconsistent heading levels across pages (TC29)
----------------------------------------------------------
`_convert_block_to_markdown_with_type` only ever assigns `text:title`
(rendered as `#`) to a heading block when
`page_num == self._get_first_text_page_num()` (pymupdf_advanced_pipeline.py
:915) -- i.e. purely because of which page a block happens to land on, not
because of its actual font size relative to the rest of the document.
Every other page's same-size heading falls through to `text:section`
(rendered as `##`) instead, producing the exact procedure_KAL-SP-06 bug
found on TC29: 16pt section headers get `#` on page 1 and `##` on pages 2-3
even though they are identically sized in the source PDF.

This patch wraps the classification method: after computing the original
`text_type`, if it was downgraded to `text:section` purely by page position
but the block's own max font size matches the document's single largest
heading-candidate font size (computed once across every page, memoized), it
is promoted back to `text:title` -- the same threshold doc2mark itself
already uses for the true first-page title, just applied consistently
across every page instead of only the first.

Fix 3a -- all-caps text below body size wrongly flagged as a heading (TC30)
------------------------------------------------------------------------------
`_has_heading_layout_signal` treats ANY all-caps line as carrying a heading
layout signal regardless of its font size (pymupdf_advanced_pipeline.py
:1055-1060: `... or features.is_all_caps`), even when that text is smaller
than the document's own body text. This is exactly why the author byline
"HELENA M. CROYDE" (9.6pt, vs. an ~10.15pt page-1 average) on
croyde_1974_braithe_order_offprint.pdf gets misclassified as a `##` section
heading. This patch requires all-caps text to be at least body-sized
(size_ratio >= 1.0) before the all-caps signal alone counts as a heading
layout signal; the bold and large-font signals are untouched.

Fix 3b -- footnotes after the first one in a merged block are dropped (TC30)
--------------------------------------------------------------------------------
When PyMuPDF's own block segmentation merges several tightly-spaced
consecutive footnotes into a single text block (confirmed directly: on page
3 of croyde_1974_braithe_order_offprint.pdf, footnotes 8, 9 and 10 are all
one PyMuPDF block), doc2mark's `pdf_to_markdown()` regex-converts only the
FIRST line of that block's content to a `[^N]:` footnote
(pymupdf_advanced_pipeline.py:2086-2093: `re.match(...); if m: ...` runs
once against the whole multi-line `content` string, and `.` does not match
`\n`, so only line 1 is ever captured) -- every subsequent footnote in the
same merged block is silently discarded. This is the confirmed root cause
of footnotes 9 and 10 vanishing from the TC30 output entirely.

This patch wraps `_extract_text_as_markdown` and, for any block classified
as `text:footnote` whose content contains more than one footnote-numbered
line, splits it into one separate `text:footnote` SimpleContent item per
footnote (grouping wrapped continuation lines with the footnote they
belong to). Each split item then flows through doc2mark's own, completely
unmodified `pdf_to_markdown()` footnote-rendering path and gets its own
correct `[^N]:` entry.

No table-extraction fix is included here: doc2mark's default
`page.find_tables()` call (strategy="lines") relies on visible ruling
lines and finds nothing on the borderless schedule_of_analysis_charges_2026
pricing table; falling back to `strategy="text"` was tested directly and,
on the whole page, misdetects ordinary body paragraphs as additional
"table" rows with the same column-population density as the real table
(see TC31 observation) -- there is no safe, general, non-fixture-specific
way to distinguish them, so no table patch is applied and TC31 is left
unpatched.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

import pymupdf
from doc2mark.core.types import SimpleContent
from doc2mark.pipelines.pymupdf_advanced_pipeline import PDFLoader

_APPLIED = False

_FULL_WIDTH_FRACTION = 0.62  # a block this wide (or wider), as a fraction of
                             # page width, is treated as a heading/footer that
                             # spans both columns rather than living in one.

_FOOTNOTE_LINE_RE = re.compile(r'^\d+[\.\)\s]')


def _document_top_heading_size(loader: "PDFLoader") -> float:
    """Largest font size seen anywhere in the document (memoized on the loader)."""
    cached = getattr(loader, "_doc2mark_fix_top_heading_size", None)
    if cached is not None:
        return cached
    top = 0.0
    for page_num in range(len(loader.doc)):
        page = loader.doc.load_page(page_num)
        text_dict = page.get_text("dict", flags=pymupdf.TEXT_PRESERVE_LIGATURES)
        for block in text_dict.get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    if span["size"] > top:
                        top = span["size"]
    loader._doc2mark_fix_top_heading_size = top
    return top


def _block_max_size(block: Dict[str, Any]) -> float:
    sizes = [span["size"] for line in block["lines"] for span in line["spans"]]
    return max(sizes) if sizes else 0.0


def apply() -> None:
    """Apply all patches once. Safe to call more than once (idempotent)."""
    global _APPLIED
    if _APPLIED:
        return
    _APPLIED = True

    # ---- Fix 3a: all-caps-alone no longer counts as a heading signal below body size.
    _original_has_heading_layout_signal = PDFLoader._has_heading_layout_signal

    def _patched_has_heading_layout_signal(self, features):
        result = _original_has_heading_layout_signal(self, features)
        if not result:
            return result
        strong_signal = (
            features.size_ratio >= 1.2
            or (features.is_bold and features.size_ratio >= 1.05)
        )
        if not strong_signal and features.is_all_caps and features.size_ratio < 1.0:
            return False
        return result

    PDFLoader._has_heading_layout_signal = _patched_has_heading_layout_signal

    # ---- Fix 2: consistent text:title vs text:section across every page, not just page 1.
    _original_classify = PDFLoader._convert_block_to_markdown_with_type

    def _patched_classify(self, block, avg_font_size, max_font_size, page_num,
                           image_bboxes, table_bboxes):
        markdown_text, text_type = _original_classify(
            self, block, avg_font_size, max_font_size, page_num, image_bboxes, table_bboxes
        )
        if text_type == "text:section":
            top_size = _document_top_heading_size(self)
            if top_size > 0 and _block_max_size(block) >= top_size - 0.5:
                text_type = "text:title"
        return markdown_text, text_type

    PDFLoader._convert_block_to_markdown_with_type = _patched_classify

    # ---- Fix 3b: split merged multi-footnote blocks so every footnote survives.
    _original_extract_text_as_markdown = PDFLoader._extract_text_as_markdown

    def _patched_extract_text_as_markdown(self, page, page_num, table_bboxes=None):
        items: List[SimpleContent] = _original_extract_text_as_markdown(
            self, page, page_num, table_bboxes
        )
        result: List[SimpleContent] = []
        for item in items:
            if item.type == "text:footnote" and "\n" in item.content:
                lines = [l for l in item.content.split("\n") if l.strip()]
                starts = [i for i, l in enumerate(lines) if _FOOTNOTE_LINE_RE.match(l.strip())]
                if len(starts) > 1:
                    groups: List[List[str]] = []
                    current: List[str] = []
                    for line in lines:
                        if _FOOTNOTE_LINE_RE.match(line.strip()) and current:
                            groups.append(current)
                            current = [line]
                        else:
                            current.append(line)
                    if current:
                        groups.append(current)
                    for group in groups:
                        result.append(SimpleContent(
                            type="text:footnote",
                            content=" ".join(l.strip() for l in group),
                            page=item.page,
                            position_y=item.position_y,
                        ))
                    continue
            result.append(item)
        return result

    PDFLoader._extract_text_as_markdown = _patched_extract_text_as_markdown

    # ---- Fix 1: column-aware reading order.
    #
    # This re-implements _process_page's body (rather than post-processing its
    # dict output) so that each text item can be positionally paired with the
    # exact block that produced it -- pairing by a y0 -> x0 lookup dict was
    # tried first and abandoned after the regression check below caught a
    # real bug: two different blocks (one per column) can share the identical
    # y0 (confirmed on bulletin_no_212.pdf page 2, both columns' top block
    # start at y0=55.135...), which silently overwrites one column's x0 with
    # the other's in a dict keyed only by y. Positional pairing sidesteps that
    # entirely, and a strict length check aborts the reorder (falling back to
    # doc2mark's original position_y-only sort for that page) whenever the
    # pairing assumption can't be verified, rather than risk a wrong order.
    _original_process_page = PDFLoader._process_page

    def _text_block_bboxes(page) -> List[tuple]:
        """bbox for every real text block, in the same raw order PyMuPDF
        returns them in -- i.e. the same order _extract_text_as_markdown
        iterates blocks in, before its own table-overlap/non-empty filtering."""
        text_dict = page.get_text("dict", flags=pymupdf.TEXT_PRESERVE_LIGATURES)
        return [
            tuple(block["bbox"])
            for block in text_dict.get("blocks", [])
            if block.get("type") == 0
        ]

    def _patched_process_page(self, page_num, extract_images=True, ocr_images=False,
                               ocr_results_map=None):
        page = self.doc.load_page(page_num)

        # The IMAGE-authoritative whole-page-OCR path returns a single
        # synthetic item with nothing to reorder -- defer to the original.
        if (ocr_images and ocr_results_map is not None
                and (page_num, -1) in ocr_results_map):
            return _original_process_page(self, page_num, extract_images, ocr_images, ocr_results_map)

        table_items, table_bboxes = self._extract_tables_as_markdown(page, page_num)
        text_items = self._extract_text_as_markdown(page, page_num, table_bboxes)
        image_items = (
            self._extract_images_simple(page, page_num, ocr_images=ocr_images,
                                         ocr_results_map=ocr_results_map)
            if extract_images else []
        )
        content_items = list(table_items) + list(text_items) + list(image_items)

        if len(content_items) >= 2:
            page_width = page.rect.width
            # _extract_text_as_markdown only skips table-overlapping blocks and
            # empty-after-conversion ones -- since every surviving PyMuPDF text
            # block here has visible text, block count should equal text_item
            # count exactly; if it doesn't for some fixture we haven't seen,
            # bail out to the original safe sort rather than guess.
            block_bboxes = _text_block_bboxes(page)
            if table_bboxes:
                block_bboxes = [
                    bb for bb in block_bboxes
                    if not any(self._bbox_overlaps(bb, tb) for tb in table_bboxes)
                ]
            block_positions = [(bb[0], bb[2] - bb[0]) for bb in block_bboxes]

            if page_width > 0 and len(block_positions) == len(text_items):
                narrow = [
                    (x0, w) for x0, w in block_positions
                    if w < _FULL_WIDTH_FRACTION * page_width
                ]
                distinct_x0s = sorted({round(x0, 1) for x0, _w in narrow})
                is_two_column = False
                mid_x = None
                if len(distinct_x0s) >= 2:
                    gaps = [
                        (distinct_x0s[i + 1] - distinct_x0s[i], distinct_x0s[i], distinct_x0s[i + 1])
                        for i in range(len(distinct_x0s) - 1)
                    ]
                    biggest_gap, left_edge, right_edge = max(gaps)
                    gap_center = (left_edge + right_edge) / 2
                    left_count = sum(1 for x0, _w in narrow if x0 <= left_edge)
                    right_count = sum(1 for x0, _w in narrow if x0 >= right_edge)
                    # A block being narrower than half the page does NOT by
                    # itself mean it lives in one of two columns -- a single-
                    # column page has plenty of short lines (headings,
                    # letterhead) at the SAME x0 as its long paragraphs. Only
                    # commit to column-aware reordering when the narrow
                    # blocks' x0 values show real evidence of two distinct
                    # clusters: a large gap, roughly centered on the page,
                    # with MULTIPLE blocks on each side (not one stray
                    # element, such as a lone page-number footer sitting to
                    # the right of an otherwise single-column page -- caught
                    # exactly this way on briefing_note_BEP-BN-2026-04.pdf,
                    # whose "Page N of 7" footer is narrow and positioned far
                    # right of the body text, and which this >=2-per-side
                    # requirement now correctly excludes). An earlier version
                    # of this patch also had no minimum-count requirement and
                    # separately mis-split a single-column fee schedule,
                    # TC31, whose short heading lines were simply narrower
                    # than its body paragraphs at the SAME x0; both were
                    # caught by re-running every TC27-TC31 fixture through
                    # the patch before adopting it (see the regression check
                    # in the TC27-32 fix-pass observation).
                    is_two_column = (
                        biggest_gap > 0.15 * page_width
                        and 0.25 * page_width < gap_center < 0.75 * page_width
                        and left_count >= 2
                        and right_count >= 2
                    )
                    mid_x = gap_center

                if is_two_column:
                    narrow_ys_idx = [i for i, (_x0, w) in enumerate(block_positions)
                                      if w < _FULL_WIDTH_FRACTION * page_width]
                    narrow_min_y = min(text_items[i].position_y for i in narrow_ys_idx)
                    narrow_max_y = max(text_items[i].position_y for i in narrow_ys_idx)

                    text_sort_info = {}
                    for i, item in enumerate(text_items):
                        x0, width = block_positions[i]
                        if width >= _FULL_WIDTH_FRACTION * page_width:
                            if item.position_y <= narrow_min_y:
                                key = (0, item.position_y)   # header
                            elif item.position_y >= narrow_max_y:
                                key = (4, item.position_y)   # footer
                            else:
                                key = (2, item.position_y)   # rare mid-page span
                        else:
                            key = (1 if x0 < mid_x else 3, item.position_y)
                        text_sort_info[id(item)] = key

                    def sort_key(content_item):
                        if id(content_item) in text_sort_info:
                            return text_sort_info[id(content_item)]
                        # Tables/images: no per-column info available (rare for
                        # this fixture set) -- keep them at their natural
                        # vertical position, spanning both columns.
                        return (2, content_item.position_y)

                    content_items.sort(key=sort_key)
                else:
                    content_items.sort(key=lambda x: x.position_y)
            else:
                content_items.sort(key=lambda x: x.position_y)
        elif content_items:
            content_items.sort(key=lambda x: x.position_y)

        simple_content = []
        for item in content_items:
            if item.type.startswith("text:"):
                simple_content.append({
                    "type": item.type, "content": item.content,
                    "page": item.page, "position_y": item.position_y,
                })
            elif item.type == "table":
                simple_content.append({
                    "type": "table", "content": item.content,
                    "page": item.page, "position_y": item.position_y,
                })
            elif item.type == "image":
                entry = {
                    "type": "image", "content": item.content,
                    "page": item.page, "position_y": item.position_y,
                }
                if item.mime_type:
                    entry["mime_type"] = item.mime_type
                simple_content.append(entry)
        return simple_content

    PDFLoader._process_page = _patched_process_page
