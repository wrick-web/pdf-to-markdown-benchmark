# Input Status

## Fixture authoring: NOT STARTED

Per the frozen spec's "What comes next": *"Fixture authoring — a separate
explicit step, on Pradip's go."* No go has been given as of this writing.
Nothing in this repository should attempt to create, select, or download
replacement fixtures for TC27–TC38 ahead of that authorization.

## Input documents: WAITING FOR INPUT

The actual test input documents for the new benchmark are expected from
**Pruthviraj & Haresh**. As of this writing, they have not been provided
to this research environment.

| TC | Fixture needed | Status |
|---|---|---|
| TC27 | Short digital-text PDF, plain paragraphs | WAITING FOR INPUT |
| TC28 | Short PDF page, two clear text columns | WAITING FOR INPUT |
| TC29 | Short PDF with styled headings/subheadings | WAITING FOR INPUT |
| TC30 | PDF page with a footnote | WAITING FOR INPUT |
| TC31 | Small PDF with one simple table | WAITING FOR INPUT |
| TC32 | Small PDF with one table spanning a page break | WAITING FOR INPUT |
| TC33 | PDF with a figure + caption | WAITING FOR INPUT |
| TC34 | PDF with a data chart + title | WAITING FOR INPUT |
| TC35 | Short scanned (image-only) PDF | WAITING FOR INPUT |
| TC36 | Digital PDF with one scanned page mixed in | WAITING FOR INPUT |
| TC37 | PDF containing mathematical equations | WAITING FOR INPUT |
| TC38 | PDF containing a code block | WAITING FOR INPUT |

## What this repository already has (not a substitute — see caveat)

`01_Benchmark_PDFs/` holds 3 real documents from the **pre-Rev2**
benchmark (a hybrid earnings report, a financial report, a scanned
research paper). These were not authored against the new TC27–TC38
fixture requirements and confirmed not to contain either C16 or C17
content: a direct grep of all output text for LaTeX-style math tokens
and code-like syntax found nothing, and independently, all 10 tools
tested against these 3 PDFs in the prior cycle reported **no equations
and no code blocks encountered** in their observations — two independent
checks agreeing these documents simply don't exercise C16/C17 at all.

**These 3 documents may end up naturally answering some TC27–TC38 test
cases once someone checks them against the exact fixture requirements**
(core rule 11: "one artifact serves as many test cases as it naturally
can") — for example PDF1/PDF2 plausibly contain ordinary digital text
(TC27), styled headings (TC29), simple and cross-page tables (TC31/TC32),
and PDF3 is a clean scan (TC35). **This has not been confirmed or acted
on.** Doing so is exactly the "fixture authoring" step that requires
Pradip's go, and re-purposing an existing document as a frozen TC fixture
is a decision for that step, not something to pre-empt here.

## What happens next once input arrives

1. Confirm Pradip's go for fixture authoring.
2. For each TC, either receive the document from Pruthviraj & Haresh or
   confirm (with sign-off) that an existing document satisfies the
   minimum fixture requirement.
3. Record the expected source truth for each tested region **before**
   running any tool (core rule 5).
4. Hash the final fixture bytes (core rule 11).
5. Only then run the candidate tools listed in `Test_Case_Registry.md`
   against each TC and produce Evidence in `04_Evidence/`.
