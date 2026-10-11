# Internship Hunt — paid internship from December 2026

This is the outreach system for Wrick Majumdar (B.Sc. CS & Statistics, Christ University, 2027). The goal is a **legitimate paid internship starting December 2026**: Bengaluru first, then remote within India. Non-software roles are the first priority.

## Files

| File | What it is |
|---|---|
| `companies.csv` | Researched companies (deduplicated) with hiring evidence, pay, December-start fit, contacts and a priority score |
| `applications.csv` | One row per outreach email: draft, send, follow-up and reply tracking |
| `email_templates.md` | Role-specific templates, plus the fact sheet of what can and can't be claimed |
| `drafts/` | Personalised drafts awaiting approval, one file per company |
| `research_sources.md` | Every company's evidence and source URLs, generated from `companies.csv` |
| `research/*.json` | Raw research output by segment (analyst, growth, research, AI/tech, funded startups, programmes) |
| `dashboard.html` | Static dashboard generated from both CSVs; open it in a browser |
| `build.py` | Merges, scores, regenerates the dashboard and sources, and lists due follow-ups (standard library only) |
| `config.example.env` | Placeholder settings. No secrets: Gmail uses the OAuth connector |
| `Wrick_Majumdar_Resume.pdf` | Resume to attach. **Git-ignored** because it contains a phone number |

## Commands

```bash
python3 build.py merge research/*.json   # add new research (keeps existing statuses)
python3 build.py score                   # re-score after editing companies.csv
python3 build.py sources                 # regenerate research_sources.md
python3 build.py dashboard               # regenerate dashboard.html
python3 build.py followups               # what needs a follow-up today
```

## Priority score (0–100)

| Factor | Points |
|---|---|
| Role category | Priority A (business/analyst/marketing/BD/content) 25 · Priority B (technical) 17 |
| Pay (target band **₹8k–15k/month**) | Overlaps band (≤ ₹25k top) 20 · undisclosed/unparsed 14 · ₹15–30k 12 · below ₹8k 6 · ₹30k+ or up to ₹1L (highly competitive) 4 · unpaid → score 0 (excluded) |
| December start | Likely 15 · Possible 10 · Unclear 6 · Unlikely 0 |
| Hiring urgency | High 15 · Medium 9 · Low 4 |
| Contact quality | Email on official site 15 · in a job post 13 · third-party 8 · careers page only 4 |
| Location | Bengaluru 10 · Remote India 8 · elsewhere 4 |

Speculative leads (funded startups with no posting) are capped at Medium urgency and "Possible" for December. Funding news alone is not evidence that a company needs interns.

## Workflow and statuses

`Discovered → Researching → High Priority → Contact Verified → Draft Ready → Awaiting Approval → Sent → (Replied | Follow-up Due | No Response) → Interview → Offer | Rejected | Closed`

1. **Research:** add JSON to `research/`, then `merge`.
2. **Contact:** use only emails that are published (official site or job post). A guessed address stays `NOT FOUND`. Apply through the posting's own channel when there is no email.
3. **Draft:** write each draft from `email_templates.md` with one verified company-specific detail. Drafts are saved in `drafts/` and, after review, as Gmail drafts.
4. **Approve:** Wrick approves each email or batch by name. Nothing is sent without approval.
5. **Send:** emails go from `wrickm19@gmail.com` only (the sender identity is checked first), with the resume attached. A row is marked `Sent` only after Gmail returns a message ID.
6. **Follow up:** follow-up 1 after 5 business days, follow-up 2 about 7 days later, then `No Response`. Stop at once after a reply, rejection or opt-out. Check Gmail for replies before every follow-up.

## Safeguards

- Each message is personalised individually, with no CC/BCC, no mass mail and no more than ~15 sends a day.
- `applications.csv` is checked for duplicates before any send. One person per company per role.
- Skip unpaid roles, "pay for training" schemes and certificate-only "virtual internships".
- **College:** confirm with Christ University before accepting an offer. Check whether a December–May internship is allowed alongside semester attendance, whether NOC or approval letters are needed, and the minimum duration and credit requirements.

## Known limitations (as of 2026-10-11)

- **The cloud environment's network policy blocks company websites.** Research came from web-search result text, so every posting must be opened and confirmed live before applying. To allow direct page checks, widen the environment's network access: <https://code.claude.com/docs/en/cloud-environments#network-access>.
- No email-verification service (bounce check) is connected. "Publicly listed" means the address was seen published; it does not mean deliverability was tested.
