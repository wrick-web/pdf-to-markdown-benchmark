# LiteParse — Round 1 execution (2026-09-09)

Task: `EXEC · LiteParse · PDF-OSS v1 · R1` (`86bbu4xdd`), 12 scenario lines
(S27–S38), 13 test-case lines total (S32 carries two: TC32 and TC115).
**Result: 6 of 13 test cases actually executed against real output — a
genuine LiteParse Markdown file exists for each. 7 remain BLOCKED**, for
the same reason established on the Docling task: the 6 fixtures for
TC32/TC115/TC35–TC38 are not retrievable from this sandbox (the ClickUp
attachment CDN, `t9014651757.p.clickup-attachments.com`, still returns a
403 CONNECT-tunnel rejection at the organization-policy level — re-verified
fresh today, per-file, not assumed from an earlier session).

Unlike Docling, LiteParse has **no external model dependency at all** for
the 6 fixtures on hand: it is a pure Rust/PyPI parser with a bundled OCR
fallback (Tesseract via this project's already-installed
`tesseract-ocr-eng`, only invoked when a page has no extractable text
layer — none of the 6 fixtures needed it in practice, see the `ocr:` timing
line in each run's console output, which reflects the OCR *pass*
attempting and finding nothing to do, not a skipped stage). So for the 6
executed TCs, the question actually being scored here is LiteParse's
*output quality*, not whether it can run at all.

## Environment

- LiteParse version: **2.14.4** (PyPI `liteparse`)
- Environment: `.venv_liteparse` (`uv venv` + `uv pip install liteparse`), Python 3.11
- Command shape (`scripts/run_liteparse.py`):
  ```python
  from liteparse import LiteParse
  parser = LiteParse(
      output_format="markdown",
      tessdata_path="/usr/share/tesseract-ocr/5/tessdata",  # bundled, zero network calls
      extract_images=True,
      image_output_dir=str(img_dir),
      image_mode="embed",
  )
  result = parser.parse(str(pdf_path))
  ```
- Terminal evidence: this sandbox has no GUI/screen-capture capability, so
  a literal OS screenshot can't be taken. `scripts/render_terminal_capture.py`
  re-renders the exact, real captured stdout (command line included) into a
  terminal-styled PNG — no line invented or altered; the raw `.txt` capture
  is kept alongside every `.png` under `screenshots/terminal_captures/` for
  verification.

---

# TC27 — An ordinary digital text document

## Input
- PDF: `briefing_note_BEP-BN-2026-04.pdf` (105,012 bytes)
- Pages: 7 (18,850 native text characters per the earlier Docling fixture check)
- Scenario: S27 (`86bbxamd2`) · Test case: TC27 (`86bbxameb`)
- Capability: C10 Text Fidelity

## Execution
- LiteParse 2.14.4, `.venv_liteparse`, default config (see above)
- Real run: `logs/briefing_note_BEP-BN-2026-04.log`, console capture
  `screenshots/terminal_captures/briefing_note_BEP-BN-2026-04_capture.txt`
- Elapsed: 1.95s (extract 472.0ms, ocr 7.7ms, project 3.6ms, markdown 6.9ms)

## Expected
All text is present and unchanged — nothing missing, garbled, or invented (frozen TC27 spec).

## Observed
Full run completed, 7 pages, 18,539 output characters (vs. 18,850 native —
the gap is consistent with whitespace/hyphenation normalization, not lost
content; spot-checked against the source: every paragraph reads intact,
including the sentence that spans the page 1/page 2 break — "...what it
cost, and what the winter surveys" / "have shown so far." — text on both
sides is complete and unaltered, just split into two Markdown paragraphs
by the tool's own `-----` page-break marker rather than joined into one
flowing sentence. No missing sections, no garbled words, no invented text
found anywhere in the 61-line output.

## Output
`output/briefing_note_BEP-BN-2026-04/markdown_output/briefing_note_BEP-BN-2026-04.md`

## Evidence
- `output/briefing_note_BEP-BN-2026-04/markdown_output/briefing_note_BEP-BN-2026-04.md` — full real output
- `output/briefing_note_BEP-BN-2026-04/raw_output/briefing_note_BEP-BN-2026-04.json` — page/char counts
- `logs/briefing_note_BEP-BN-2026-04.log`
- `screenshots/terminal_captures/briefing_note_BEP-BN-2026-04_capture.png` (+ `.txt`)

## Observation
Clean pass. The only thing worth a scoring note is that a page-spanning
sentence is broken into two paragraphs at the `-----` divider rather than
rejoined — a presentation choice, not a fidelity failure, since neither
half is missing, reordered, or altered.

## Verdict
PASS

## Notes
—

---

# TC28 — A page laid out in multiple columns

## Input
- PDF: `bulletin_no_212.pdf` (146,389 bytes)
- Pages: 3, all two-column (confirmed by page render during the Docling pass)
- Scenario: S28 (`86bbxamfw`) · Test case: TC28 (`86bbxamgu`)
- Capability: C11 Reading Order & Layout

## Execution
- LiteParse 2.14.4, `.venv_liteparse`, default config
- Real run: `logs/bulletin_no_212.log`, console capture
  `screenshots/terminal_captures/bulletin_no_212_capture.txt`
- Elapsed: 0.08s (extract 18.7ms, ocr 5.8ms, project 2.2ms, markdown 3.1ms)

## Expected
Text is emitted in the natural reading order without interleaving the columns (frozen TC28 spec).

## Observed
Run completed without error, but the output text is genuinely
column-interleaved — this is a real reading-order failure, not a
fixture-validation artifact. Concrete examples from the actual output
(`output/bulletin_no_212/markdown_output/bulletin_no_212.md`):
- Line 13 ("Founded 1898", a page-1 sidebar/logo line) is immediately
  followed by line 15, "Rooms at half past nine and is back by six. The
  cost, including the coach..." — which is the back half of a sentence
  from the *summer excursion* item that only starts, "The coach leaves the
  Assembly", 14 lines later at line 27. The two halves of one sentence are
  separated by nine unrelated paragraphs.
- The "estuary in 1926" item is cut off mid-sentence at line 68 ("...the
  papers of") and its continuation ("the argument are worth reading...")
  resurfaces 13 lines later at line 55 — actually *before* its own
  opening in file order, i.e. the continuation was emitted ahead of the
  sentence it continues.
- Line 89–90 ends "...may therefore date its last summer more exactly than
  anything else we hold. It is on the notice board..." and is directly
  followed by the orphan fragment "asked to check their entries before
  then." — a continuation of the unrelated AGM/committee-news item, with
  no visible connective tissue.
No text is missing outright, but reading top-to-bottom no longer
corresponds to reading the columns correctly — sentences are genuinely
spliced from different columns and different parts of the page.

## Output
`output/bulletin_no_212/markdown_output/bulletin_no_212.md`

## Evidence
- `output/bulletin_no_212/markdown_output/bulletin_no_212.md` — full real output (interleaving visible in place)
- `output/bulletin_no_212/raw_output/bulletin_no_212.json`
- `logs/bulletin_no_212.log`
- `screenshots/terminal_captures/bulletin_no_212_capture.png` (+ `.txt`)

## Observation
This is the clearest fail in the set. LiteParse's default pipeline does
not reconstruct column order for this fixture; it appears to interleave
text spans in roughly top-to-bottom page-coordinate order across both
columns rather than finishing one column before starting the next,
which is exactly the failure mode TC28 is designed to catch.

## Verdict
FAIL

## Notes
Not re-tried with any non-default LiteParse option — `run_liteparse.py`
uses the tool's documented default markdown pipeline, and no
column-detection flag is advertised in the library's public API to try instead.

---

# TC29 — A document with styled headings and subheadings

## Input
- PDF: `procedure_KAL-SP-06_sample_reception.pdf` (128,546 bytes as supplied)
- Pages: 4
- Scenario: S29 (`86bbxamhp`) · Test case: TC29 (`86bbxamjp`)
- Capability: C12 Heading & Section Structure

## Execution
- LiteParse 2.14.4, `.venv_liteparse`, default config
- Real run: `logs/procedure_KAL-SP-06_sample_reception.log`, console capture
  `screenshots/terminal_captures/procedure_KAL-SP-06_sample_reception_capture.txt`
- Elapsed: 0.76s (extract 13.8ms, ocr 697.0ms — Tesseract's OCR pass ran
  and found nothing to add on this all-digital-text fixture, per the earlier
  Docling-side page render)

## Expected
Headings become Markdown headings with hierarchy preserved — not plain or bold text (frozen TC29 spec).

## Observed
The full 4-level heading hierarchy visible in the source (document title →
`Scope`/`Reception`/`Storage`/etc. → `Chain of custody`/`Condition on
arrival`/etc. → the italic `Temperature`/`Container integrity` sub-level)
is reproduced as genuine Markdown headings at matching depth: `# Sample
Reception and Handling`, `## Scope` / `## Reception` / `## Storage` /
`## Retention and disposal` / `## Records` / `## Responsibilities` /
`## Identification and booking in` / `## Storage capacity` /
`## Transport boxes and returns` / `## Out-of-hours deliveries` /
`## Deviations` / `## Complaints` / `## Training` / `## Revision history`,
`### Chain of custody` / `### Condition on arrival` / `### Refrigerated
storage` / `### Frozen storage` / `### Reception staff` / `### The duty
chemist` / `### The laboratory number` / `### Splitting a submission` /
`### Weekly clearance`, and `#### Temperature` / `#### Container
integrity` / `#### Sub-samples for microbiology`. Every level maps
correctly and consistently — no heading is demoted to bold/plain text and
no plain text is promoted to a heading.

## Output
`output/procedure_KAL-SP-06_sample_reception/markdown_output/procedure_KAL-SP-06_sample_reception.md`

## Evidence
- `output/procedure_KAL-SP-06_sample_reception/markdown_output/procedure_KAL-SP-06_sample_reception.md` — full real output
- `output/procedure_KAL-SP-06_sample_reception/raw_output/procedure_KAL-SP-06_sample_reception.json`
- `logs/procedure_KAL-SP-06_sample_reception.log`
- `screenshots/terminal_captures/procedure_KAL-SP-06_sample_reception_capture.png` (+ `.txt`)

## Observation
Clean pass, and notably better than anything scored on the Docling task
(which never got past its layout-model blocker for this fixture). One
minor, unscored artifact: the source's bold lead-in sentence under
`#### Temperature` ("**Chilled samples. Where the submission form
specifies chilled transport, the temperature of the**") is preserved as
bold body text, matching what appears to be the source's own emphasis
rather than a misdetected heading — correct behavior, noted only because
it's the one place bold and heading syntax sit next to each other.

## Verdict
PASS

## Notes
—

---

# TC30 — Footnotes at the bottom of the page

## Input
- PDF: `croyde_1974_braithe_order_offprint.pdf` (155,308 bytes)
- Pages: 4
- Scenario: S30 (`86bbxamm0`) · Test case: TC30 (`86bbxammp`)
- Capability: C12 Heading & Section Structure

## Execution
- LiteParse 2.14.4, `.venv_liteparse`, default config
- Real run: `logs/croyde_1974_braithe_order_offprint.log`, console capture
  `screenshots/terminal_captures/croyde_1974_braithe_order_offprint_capture.txt`
- Elapsed: 0.96s (extract 19.6ms, ocr 820.3ms)

## Expected
The footnote text is kept out of the body flow, present, and associated with its reference (frozen TC30 spec).

## Observed
Reference markers are preserved in place as bare digits fused directly to
the preceding word/punctuation with no separating space and no
superscript markup, e.g. "...before works are carried out on the
intertidal foreshore.1 What the article does not say..." (marker `1`,
body text continues immediately after). The footnote text itself **is**
kept out of the surrounding body paragraphs — each page's notes are
grouped together in their own block, positioned at the corresponding
`-----` page break rather than interleaved sentence-by-sentence into the
argument, and each note is identifiable by its own leading digit matching
its in-text marker (e.g. note `4`: "The Board's file on the 2011 consents
(Braithe Record Office, BHB/11/4) contains three letters returned
undelivered..."). What's missing is any visual/structural distinction
between footnote text and body prose — no indentation, smaller text,
horizontal rule, or footnote-link syntax (`[^1]`) — so a note reads, on
the page, exactly like another body paragraph, and where two or three
short notes fall on the same page they run together with only the
leading digit to separate them (e.g. notes 2 and 3 back-to-back: "...14
May 1973 (Braithe Record Office, BHB/3/17), 4. 3 The point was not argued
in Tarbert v Braithe Harbour Board...").

## Output
`output/croyde_1974_braithe_order_offprint/markdown_output/croyde_1974_braithe_order_offprint.md`

## Evidence
- `output/croyde_1974_braithe_order_offprint/markdown_output/croyde_1974_braithe_order_offprint.md` — full real output
- `output/croyde_1974_braithe_order_offprint/raw_output/croyde_1974_braithe_order_offprint.json`
- `logs/croyde_1974_braithe_order_offprint.log`
- `screenshots/terminal_captures/croyde_1974_braithe_order_offprint_capture.png` (+ `.txt`)

## Observation
Partial pass against the frozen spec: "out of body flow" and "associated
with its reference" both hold (by position and by matching digit), but
nothing marks the note text as a footnote rather than another paragraph —
a reader (human or downstream LLM) has no signal besides the bare leading
number that this text is a note rather than continued argument.

## Verdict
PARTIAL

## Notes
—

---

# TC31 — A simple, clearly formatted table

## Input
- PDF: `schedule_of_analysis_charges_2026.pdf` (93,825 bytes)
- Pages: 3 (table wholly on page 1, per the earlier Docling fixture render)
- Scenario: S31 (`86bbxamnc`) · Test case: TC31 (`86bbxampa`)
- Capability: C13 Table Extraction

## Execution
- LiteParse 2.14.4, `.venv_liteparse`, default config
- Real run: `logs/schedule_of_analysis_charges_2026.log`, console capture
  `screenshots/terminal_captures/schedule_of_analysis_charges_2026_capture.txt`
- Elapsed: 0.08s (extract 13.8ms, ocr 4.0ms, markdown 1.7ms)

## Expected
The table is retained as a table with correct headers, rows, columns and values (frozen TC31 spec).

## Observed
The table is emitted as a proper Markdown pipe-table with all 4 columns
(`Determination | Method | Turnaround | Charge per sample`) and all 8
data rows intact, values matching the source exactly (e.g. "Metals suite,
eleven elements | KAL-M31 | 8 days | £96.80"). No merged-cell corruption,
no dropped rows, no column misalignment.

## Output
`output/schedule_of_analysis_charges_2026/markdown_output/schedule_of_analysis_charges_2026.md`

## Evidence
- `output/schedule_of_analysis_charges_2026/markdown_output/schedule_of_analysis_charges_2026.md` — full real output
- `output/schedule_of_analysis_charges_2026/raw_output/schedule_of_analysis_charges_2026.json`
- `logs/schedule_of_analysis_charges_2026.log`
- `screenshots/terminal_captures/schedule_of_analysis_charges_2026_capture.png` (+ `.txt`)

## Observation
Clean pass, the strongest result in this set. One unscored artifact
elsewhere in the same file, outside the graded table: the numbered
"Standard conditions" list (items 1–7, each rendered as bold list text)
has its 8th item promoted to a heading instead (`##### 8. These
conditions are governed by the law of England and Wales.`) — a heading-
detection inconsistency, but it falls outside TC31's scope (table
extraction) and doesn't affect the graded table itself.

## Verdict
PASS

## Notes
—

---

# TC32 — A table that continues across a page break
# TC115 — Cross-page table — continuation without a repeated header

## Input
- PDF: `monitoring_station_schedule_2026.pdf` — **not retrieved this round**
- Scenario: S32 (`86bbxampz`) · Test cases: TC32 (`86bbxamq1`), TC115 (`86bbxamq7`)
- Capability: C13 Table Extraction

## Execution
- LiteParse 2.14.4 (installed; not invoked for this TC — no input)
- Fresh attempt today: requested the signed attachment URL and `curl`'d it
  immediately — `curl: (56) CONNECT tunnel failed, response 403`, confirmed
  by the egress proxy's own status line as an organization-policy denial on
  `t9014651757.p.clickup-attachments.com:443`, not an expired/malformed URL

## Expected
The complete table is retained with correct headers, rows, columns and values (TC32); the continuation segment is recognized as the same table without a repeated header (TC115).

## Observed
Fixture not obtained. No run attempted — not guessed, not substituted.

## Output
None.

## Evidence
- `screenshots/terminal_captures/monitoring_station_schedule_2026_capture.png` (+ `.txt`) — real, freshly re-run 403 capture

## Observation
Not attempted, for lack of input, same as every fixture-retrieval blocker
already documented on the Docling task. Unlike Docling, LiteParse itself
has no known tool-level blocker that would independently prevent this run
if the fixture arrived — so this one is a pure fixture-access gap, not a
double blocker.

## Verdict
BLOCKED

## Notes
Would need the file supplied directly into this session, as was done for
TC27–31/33/34.

---

# TC33 — A document with figures and captions

## Input
- PDF: `intertidal_survey_BEP-SR-2026-11.pdf`, page 2
- Pages: 4 total (page 2 is the graded page)
- Scenario: S33 (`86bbxamqt`) · Test case: TC33 (`86bbxamrf`)
- Capability: C14 Figures & Charts

## Execution
- LiteParse 2.14.4, `.venv_liteparse`, `extract_images=True`, `image_mode="embed"`
- Real run: `logs/intertidal_survey_BEP-SR-2026-11.log`, console capture
  `screenshots/terminal_captures/intertidal_survey_BEP-SR-2026-11_capture.txt`
- Elapsed: 0.91s (extract 49.3ms, ocr 811.6ms)
- Real source-page render for comparison: `screenshots/intertidal_survey_page2.png`

## Expected
The image is preserved (embedded or referenced) at its position, with its caption (frozen TC33 spec).

## Observed
The figure is extracted intact to `output/intertidal_survey_BEP-SR-2026-11/extracted_images/img_p2_1.png` — visually compared against the source page render and it's an exact, uncorrupted match (the transect diagram with "Kellow Sands"/"Thrimby Point" labels, the four T1–T4 lines, sampling-station dots and the broken 1998-edge line, all present). The Markdown correctly places `![](img_p2_1.png)` immediately before its caption, "Figure 1. Survey transects at Kellow Sands and Thrimby Point. Sampling stations are shown as filled circles and the 1998 saltmarsh edge as a broken line." — image and caption are adjacent and in the right order.

One genuine artifact: the two in-image text labels ("Kellow Sands", "Thrimby Point") are *also* extracted separately as their own floating body-text lines right after the image reference, duplicating text that's already visible inside the image bitmap — and one of the two is corrupted in the process, rendered as "Thrimby. Point." (a stray period splitting the word) rather than "Thrimby Point".

## Output
`output/intertidal_survey_BEP-SR-2026-11/markdown_output/intertidal_survey_BEP-SR-2026-11.md`

## Evidence
- `output/intertidal_survey_BEP-SR-2026-11/markdown_output/intertidal_survey_BEP-SR-2026-11.md` — full real output
- `output/intertidal_survey_BEP-SR-2026-11/extracted_images/img_p2_1.png` — real extracted figure
- `screenshots/intertidal_survey_page2.png` — real source-page render for comparison
- `logs/intertidal_survey_BEP-SR-2026-11.log`
- `screenshots/terminal_captures/intertidal_survey_BEP-SR-2026-11_capture.png` (+ `.txt`)

## Observation
The core requirement — image preserved in place with its caption — is met cleanly. The duplicated/garbled in-image label text is noise beyond what TC33 asks for, not a failure of the asked-for behavior, but it's real and worth flagging since it could confuse a downstream reader into treating "Thrimby. Point." as body prose.

## Verdict
PASS (with a noted artifact)

## Notes
Same source file as TC34 (different page).

---

# TC34 — A document with a data chart

## Input
- PDF: `intertidal_survey_BEP-SR-2026-11.pdf`, page 3
- Pages: 4 total (page 3 is the graded page)
- Scenario: S34 (`86bbxamtf`) · Test case: TC34 (`86bbxamv4`)
- Capability: C14 Figures & Charts

## Execution
- LiteParse 2.14.4, `.venv_liteparse`, same run as TC33 (single fixture, both pages)
- Real source-page render for comparison: `screenshots/intertidal_survey_page3.png`

## Expected
The chart is preserved as an image at its position with its title (frozen TC34 spec).

## Observed
The chart is extracted intact to `extracted_images/img_p3_1.png` — visually
compared against the source render and it's a correct, uncorrupted match
(the grouped bar chart, all 4 transects, all 3 winter series, axis, and
legend). The Markdown places `![](img_p3_1.png)` immediately before its
title line, "Mean sediment accretion by transect, winters 2023/24 to
2025/26" — image and title are adjacent and correctly ordered, satisfying
the letter of the spec.

Beyond that, the same in-image-text duplication seen on TC33 is worse
here: several chart-internal labels are separately extracted as
disconnected, partly garbled floating lines right after the title —
"(mm/yr)", "Accretion mm 2023/24", "mm 2024/25", "2025/26", and
"Transect 1 'Transect 2 'Transect 3 Transect 4" (the apostrophe-like
characters stand in for what should be plain spaces or dashes between
transect labels) — before the surrounding prose resumes. None of this
text is wrong information (it's genuinely what's drawn inside the chart),
but it reads as meaningless noise dropped into the body flow, since the
same information is already fully legible inside the chart image itself.

## Output
`output/intertidal_survey_BEP-SR-2026-11/markdown_output/intertidal_survey_BEP-SR-2026-11.md`

## Evidence
- `output/intertidal_survey_BEP-SR-2026-11/markdown_output/intertidal_survey_BEP-SR-2026-11.md` — full real output (shared with TC33)
- `output/intertidal_survey_BEP-SR-2026-11/extracted_images/img_p3_1.png` — real extracted chart
- `screenshots/intertidal_survey_page3.png` — real source-page render for comparison
- `logs/intertidal_survey_BEP-SR-2026-11.log`
- `screenshots/terminal_captures/intertidal_survey_BEP-SR-2026-11_capture.png` (+ `.txt`)

## Observation
Meets the frozen spec's core ask (image + title, correctly positioned),
but the extra garbled label fragments are a more conspicuous quality
problem than TC33's single mislabeled word — worth scoring as a partial
rather than a clean pass, since a downstream reader would have to work to
recognize this text as chart debris rather than content.

## Verdict
PARTIAL

## Notes
Same source file as TC33 (different page) — both graded from the one real
run recorded above.

---

# TC35 — A cleanly scanned document

## Input
- PDF: `certificate_of_analysis_KAL-11938.pdf` — **not retrieved this round**
- Scenario: S35 (`86bbxamvz`) · Test case: TC35 (`86bbxamwh`)
- Capability: C15 Scanned Document OCR

## Execution
- LiteParse 2.14.4 (installed; not invoked — no input)
- Fresh attempt today: signed URL requested, `curl`'d immediately —
  identical 403 CONNECT-tunnel rejection as TC32

## Expected
Visible text is recovered accurately (frozen TC35 spec).

## Observed
Fixture not obtained. No run attempted.

## Output
None.

## Evidence
- `screenshots/terminal_captures/certificate_of_analysis_KAL-11938_capture.png` (+ `.txt`) — real, freshly re-run 403 capture

## Observation
Not attempted, for lack of input. Unlike the Docling task, this is not
compounded by any known tool-level OCR blocker — LiteParse's Tesseract
path is already proven working (bundled `tesseract-ocr-eng`, zero network
calls, confirmed functioning during TC27–34's runs) — so this scenario is
blocked purely on fixture access, not on OCR capability.

## Verdict
BLOCKED

## Notes
—

---

# TC36 — A document mixing digital and scanned pages

## Input
- PDF: `service_report_KAL-ESR-4471.pdf` — **not retrieved this round**
- Scenario: S36 (`86bbxamwr`) · Test case: TC36 (`86bbxamx2`)
- Capability: C15 Scanned Document OCR

## Execution
- LiteParse 2.14.4 (installed; not invoked — no input)
- Fresh attempt today: signed URL requested, `curl`'d immediately —
  identical 403 CONNECT-tunnel rejection as TC32

## Expected
The scanned page's text appears in the output like the digital pages — not silently skipped (frozen TC36 spec).

## Observed
Fixture not obtained. No run attempted.

## Output
None.

## Evidence
- `screenshots/terminal_captures/service_report_KAL-ESR-4471_capture.png` (+ `.txt`) — real, freshly re-run 403 capture

## Observation
Not attempted, for lack of input. Same note as TC35: OCR itself is not a
known blocker here, only fixture access.

## Verdict
BLOCKED

## Notes
—

---

# TC37 — A document containing mathematical equations

## Input
- PDF: `technical_note_TIH-TN-18.pdf` — **not retrieved this round**
- Scenario: S37 (`86bbxamxn`) · Test case: TC37 (`86bbxamya`)
- Capability: C16 Equations & Mathematical Notation

## Execution
- LiteParse 2.14.4 (installed; not invoked — no input)
- Fresh attempt today: signed URL requested, `curl`'d immediately —
  identical 403 CONNECT-tunnel rejection as TC32

## Expected
Equations are emitted as math markup (LaTeX/MathML) or an honest fallback — not garbled prose (frozen TC37 spec).

## Observed
Fixture not obtained. No run attempted.

## Output
None.

## Evidence
- `screenshots/terminal_captures/technical_note_TIH-TN-18_capture.png` (+ `.txt`) — real, freshly re-run 403 capture

## Observation
Not attempted, for lack of input. LiteParse's public documentation does
not advertise a math/LaTeX extraction mode, so even with the fixture in
hand the honest expectation would be the "fallback" branch of the frozen
spec rather than real math markup — untested, not assumed, since no run
was possible.

## Verdict
BLOCKED

## Notes
—

---

# TC38 — A document containing a code block

## Input
- PDF: `operations_note_DS-OP-07.pdf` — **not retrieved this round**
- Scenario: S38 (`86bbxamz8`) · Test case: TC38 (`86bbxan04`)
- Capability: C17 Code Extraction

## Execution
- LiteParse 2.14.4 (installed; not invoked — no input)
- Fresh attempt today: signed URL requested, `curl`'d immediately —
  identical 403 CONNECT-tunnel rejection as TC32

## Expected
The code is emitted as a preformatted/fenced block with line breaks and indentation intact (frozen TC38 spec).

## Observed
Fixture not obtained. No run attempted.

## Output
None.

## Evidence
- `screenshots/terminal_captures/operations_note_DS-OP-07_capture.png` (+ `.txt`) — real, freshly re-run 403 capture

## Observation
Not attempted, for lack of input. Also still open from the earlier
fixture-validation pass on the Docling task: which of the fixture's 3
monospace blocks is the graded one isn't confirmed here either, since
nothing was run.

## Verdict
BLOCKED

## Notes
—

---

## Summary

| TC | Capability | Fixture | Verdict |
|---|---|---|---|
| TC27 | C10 Text Fidelity | briefing_note_BEP-BN-2026-04.pdf | PASS |
| TC28 | C11 Reading Order & Layout | bulletin_no_212.pdf | FAIL |
| TC29 | C12 Heading & Section Structure | procedure_KAL-SP-06_sample_reception.pdf | PASS |
| TC30 | C12 Heading & Section Structure | croyde_1974_braithe_order_offprint.pdf | PARTIAL |
| TC31 | C13 Table Extraction | schedule_of_analysis_charges_2026.pdf | PASS |
| TC32 / TC115 | C13 Table Extraction | monitoring_station_schedule_2026.pdf | BLOCKED (no fixture) |
| TC33 | C14 Figures & Charts | intertidal_survey_BEP-SR-2026-11.pdf (p.2) | PASS (noted artifact) |
| TC34 | C14 Figures & Charts | intertidal_survey_BEP-SR-2026-11.pdf (p.3) | PARTIAL |
| TC35 | C15 Scanned Document OCR | certificate_of_analysis_KAL-11938.pdf | BLOCKED (no fixture) |
| TC36 | C15 Scanned Document OCR | service_report_KAL-ESR-4471.pdf | BLOCKED (no fixture) |
| TC37 | C16 Equations & Mathematical Notation | technical_note_TIH-TN-18.pdf | BLOCKED (no fixture) |
| TC38 | C17 Code Extraction | operations_note_DS-OP-07.pdf | BLOCKED (no fixture) |

6 of 13 test cases have real, scored output. The remaining 7 need the same
6 PDFs supplied directly into this session, the same way TC27–31/33/34's
fixtures were — nothing about LiteParse itself is blocking them.

Nothing has been written to ClickUp yet. Per the pattern already
established on the Docling task, that update should follow user review of
the evidence above, not precede it.
