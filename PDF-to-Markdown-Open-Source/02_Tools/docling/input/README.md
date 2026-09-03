# input/ — empty

The assigned TC27 fixture (`briefing_note_BEP-BN-2026-04.pdf`, from
ClickUp task `86bbr4dmu`) could not be retrieved into this sandbox —
see `../observations.md` for the exact blocker. Nothing was substituted
in its place. This folder is intentionally empty pending fixture access.

Re-checked the same day, this session, with a freshly issued
`clickup_download_task_attachment` signed URL and an immediate `curl`:
still a 403/`connect_rejected` at the organization-policy level (see
`../observations.md` → "Re-verification pass"). Not a stale-URL issue.
