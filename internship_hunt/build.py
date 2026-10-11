#!/usr/bin/env python3
"""Merge research JSON -> companies.csv (scored, deduplicated), and render dashboard.html.

Usage:
  python3 build.py merge research/*.json   # add/refresh companies from research files
  python3 build.py score                   # re-score companies.csv in place
  python3 build.py dashboard               # regenerate dashboard.html from both CSVs
  python3 build.py sources                 # regenerate research_sources.md
  python3 build.py followups               # list follow-ups due today or earlier

Standard library only.
"""
import csv
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPANIES = HERE / "companies.csv"
APPLICATIONS = HERE / "applications.csv"
DASHBOARD = HERE / "dashboard.html"

COMPANY_FIELDS = [
    "id", "company", "website", "industry", "size", "location", "work_mode",
    "best_fit_role", "role_category", "why_relevant", "vacancy_type",
    "hiring_evidence", "hiring_urgency", "urgency_reason", "source_urls",
    "date_checked", "december_start", "stipend", "paid_status", "duration",
    "contact_name", "contact_title", "contact_email", "email_status",
    "email_source", "linkedin_or_careers_url", "outreach_angle",
    "priority_score", "status", "segment", "notes",
]

APPLICATION_FIELDS = [
    "company_id", "company", "role", "recipient_name", "recipient_title",
    "recipient_email", "subject", "status", "gmail_draft_id", "gmail_message_id",
    "gmail_thread_id", "first_contact_date", "followup_1_due", "followup_1_sent",
    "followup_2_due", "followup_2_sent", "reply_status", "last_reply_date",
    "stipend", "location", "sources", "notes",
]

STATUSES = [
    "Discovered", "Researching", "High Priority", "Contact Verified",
    "Draft Ready", "Awaiting Approval", "Sent", "Replied", "Follow-up Due",
    "Interview", "Offer", "Rejected", "No Response", "Closed",
]


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.I)


def norm_key(name):
    return re.sub(r"[^a-z0-9]", "", name.lower().replace("pvt", "").replace("ltd", ""))


TARGET_STIPEND = (8000, 15000)  # Wrick's target band, INR/month (set 2026-10-11)


def stipend_range(text):
    """Parse '₹10,000–22,000/month', 'Rs 15K', 'Up to Rs 1,00,000' -> (low, high) INR, or None."""
    t = text.lower().replace(",", "")
    nums = []
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*(k|l|lakh)?\b", t):
        n = float(m.group(1)) * {"k": 1e3, "l": 1e5, "lakh": 1e5}.get(m.group(2) or "", 1)
        if 1000 <= n <= 300000:
            nums.append(n)
    if not nums:
        return None
    low = 0 if "up to" in t or "upto" in t else min(nums)
    return low, max(nums)


def pay_points(paid, stipend):
    """Favour the 8-15k band; competitive high-stipend roles and sub-8k roles score lower."""
    if paid.startswith("Unpaid"):
        return 0
    rng = stipend_range(stipend) if paid.startswith("Confirmed") else None
    if not rng:
        return 14 if paid.startswith("Confirmed") or "Undisclosed" in paid else 0
    low, high = rng
    lo_t, hi_t = TARGET_STIPEND
    if high < lo_t:
        return 6           # below the floor
    if low <= hi_t and high >= lo_t and high <= 25000:
        return 20          # overlaps the target band
    if low <= 25000 and high <= 30000:
        return 12          # a bit above target: fine, more competitive
    return 4               # 30k+ / up to 1L: highly competitive, deprioritised


def score(row):
    """Transparent 0-100 priority score. See README for the rubric."""
    s = 0
    s += 25 if row.get("role_category", "").strip().upper() == "A" else 17
    paid = row.get("paid_status", "")
    s += pay_points(paid, row.get("stipend", ""))
    dec = row.get("december_start", "").lower()
    speculative = row.get("vacancy_type", "").lower().startswith("spec")
    if speculative and dec.startswith("likely"):
        dec = "possible"  # nobody has confirmed a December start for an unadvertised role
    s += 15 if dec.startswith("likely") else 10 if dec.startswith("possible") else 0 if dec.startswith("unlikely") else 6
    urg = row.get("hiring_urgency", "").lower()
    if speculative and urg.startswith("high"):
        urg = "medium"  # funding news is not direct evidence of intern demand
    s += 15 if urg.startswith("high") else 9 if urg.startswith("medium") else 4
    es = row.get("email_status", "")
    if row.get("contact_email") and "official" in es:
        s += 15
    elif row.get("contact_email") and "job post" in es:
        s += 13
    elif row.get("contact_email"):
        s += 8
    elif row.get("linkedin_or_careers_url"):
        s += 4
    loc = (row.get("location", "") + " " + row.get("work_mode", "")).lower()
    s += 10 if ("bengaluru" in loc or "bangalore" in loc) else 8 if "remote" in loc else 4
    if paid.startswith("Unpaid"):
        s = 0
    return min(s, 100)


def read_csv(path, fields):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [{k: r.get(k, "") or "" for k in fields} for r in csv.DictReader(f)]


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def merge(paths):
    rows = read_csv(COMPANIES, COMPANY_FIELDS)
    index = {norm_key(r["company"]): r for r in rows}
    next_id = max([int(r["id"][1:]) for r in rows if r["id"][1:].isdigit()] + [0]) + 1
    added = 0
    for p in paths:
        seg = Path(p).stem
        for item in json.loads(Path(p).read_text(encoding="utf-8")):
            item = {k: str(v).strip() if v is not None else "" for k, v in item.items()}
            if not EMAIL_RE.match(item.get("contact_email", "")):
                item["contact_email"] = ""  # "NOT FOUND" or junk: treat as no email
            if not item.get("company"):
                continue
            if item.get("paid_status", "").lower().startswith("unpaid"):
                continue
            key = norm_key(item["company"])
            if key in index:
                existing = index[key]
                # Keep existing status; fill blanks; note the extra source.
                if item.get("contact_email") and not existing["contact_email"]:
                    for k in ("contact_name", "contact_title", "contact_email", "email_status", "email_source"):
                        existing[k] = item.get(k, "")
                for k in COMPANY_FIELDS:
                    if not existing.get(k) and item.get(k):
                        existing[k] = item[k]
                if item.get("source_urls") and item["source_urls"] not in existing["source_urls"]:
                    existing["source_urls"] += " " + item["source_urls"]
                if seg not in existing["segment"]:
                    existing["segment"] += ";" + seg
                continue
            row = {k: item.get(k, "") for k in COMPANY_FIELDS}
            row["id"] = f"C{next_id:03d}"
            row["segment"] = seg
            row["status"] = "Discovered"
            next_id += 1
            index[key] = row
            rows.append(row)
            added += 1
    # Deduplicate emails: the same address must not be used for two companies.
    seen = {}
    for r in rows:
        e = r["contact_email"].lower()
        if e and e in seen:
            r["notes"] = (r["notes"] + f" | DUPLICATE EMAIL of {seen[e]}").strip(" |")
        elif e:
            seen[e] = r["id"]
    rescore(rows)
    print(f"merged: {added} new, {len(rows)} total")


def rescore(rows=None):
    write_back = rows is None
    rows = rows if rows is not None else read_csv(COMPANIES, COMPANY_FIELDS)
    for r in rows:
        r["priority_score"] = str(score(r))
        if r["status"] in ("", "Discovered", "Researching", "High Priority", "Contact Verified"):
            if int(r["priority_score"]) >= 70:
                r["status"] = "Contact Verified" if r["contact_email"] else "High Priority"
    rows.sort(key=lambda r: -int(r["priority_score"]))
    write_csv(COMPANIES, COMPANY_FIELDS, rows)
    if write_back:
        print(f"rescored {len(rows)} rows")


def add_business_days(d, n):
    while n:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def followups():
    today = dt.date.today()
    apps = read_csv(APPLICATIONS, APPLICATION_FIELDS)
    due = []
    for a in apps:
        if a["status"] in ("Rejected", "Closed", "Offer", "Interview", "Replied"):
            continue
        for n in ("1", "2"):
            d = a[f"followup_{n}_due"]
            if d and not a[f"followup_{n}_sent"] and dt.date.fromisoformat(d) <= today:
                due.append((a["company"], a["recipient_email"], n, d))
                break
    for c, e, n, d in due:
        print(f"Follow-up {n} due {d}: {c} <{e}>")
    if not due:
        print("No follow-ups due.")
    return due


def dashboard():
    comps = read_csv(COMPANIES, COMPANY_FIELDS)
    apps = read_csv(APPLICATIONS, APPLICATION_FIELDS)
    today = dt.date.today().isoformat()
    sent_states = {"Sent", "Replied", "Follow-up Due", "Interview", "Offer", "Rejected", "No Response"}
    stats = [
        ("Companies researched", len(comps)),
        ("Paid confirmed", sum(c["paid_status"].startswith("Confirmed") for c in comps)),
        ("High-priority (score ≥ 70)", sum(int(c["priority_score"] or 0) >= 70 for c in comps)),
        ("Drafts awaiting approval", sum(a["status"] in ("Draft Ready", "Awaiting Approval") for a in apps)),
        ("Emails sent", sum(a["status"] in sent_states for a in apps)),
        ("Responses", sum(bool(a["reply_status"]) and a["reply_status"] != "None" for a in apps)),
        ("Interviews / offers", sum(a["status"] in ("Interview", "Offer") for a in apps)),
        ("Follow-ups due", sum(
            any(a[f"followup_{n}_due"] and not a[f"followup_{n}_sent"] and a[f"followup_{n}_due"] <= today for n in "12")
            and a["status"] in ("Sent", "Follow-up Due", "No Response") for a in apps)),
    ]
    e = html.escape
    tiles = "".join(f'<div class="tile"><div class="n">{v}</div><div class="l">{e(k)}</div></div>' for k, v in stats)

    def link(u):
        u = u.split()[0] if u else ""
        return f'<a href="{e(u)}" target="_blank" rel="noopener">source</a>' if u.startswith("http") else ""

    crow = "".join(
        f"<tr><td>{e(c['priority_score'])}</td><td><b>{e(c['company'])}</b><br><small>{e(c['industry'])}</small></td>"
        f"<td>{e(c['best_fit_role'])}</td><td>{e(c['location'])}<br><small>{e(c['work_mode'])}</small></td>"
        f"<td>{e(c['paid_status'])}<br><small>{e(c['stipend'])}</small></td><td>{e(c['hiring_urgency'])}</td>"
        f"<td>{e(c['december_start'][:40])}</td><td>{e(c['contact_email'] or 'NOT FOUND')}<br><small>{e(c['email_status'])}</small></td>"
        f"<td>{e(c['status'])}</td><td>{link(c['source_urls'])}</td></tr>"
        for c in comps)
    arow = "".join(
        f"<tr><td>{e(a['company'])}</td><td>{e(a['recipient_email'])}</td><td>{e(a['subject'])}</td><td>{e(a['status'])}</td>"
        f"<td>{e(a['first_contact_date'])}</td><td>{e(a['followup_1_due'])}</td><td>{e(a['reply_status'])}</td></tr>"
        for a in apps)
    DASHBOARD.write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Internship Hunt Dashboard</title>
<style>
:root{{--bg:#fafaf9;--fg:#1c1917;--muted:#78716c;--card:#fff;--line:#e7e5e4;--accent:#0f766e}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1c1917;--fg:#f5f5f4;--muted:#a8a29e;--card:#292524;--line:#44403c;--accent:#5eead4}}}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,sans-serif}}
h1{{font-size:20px;margin:0 0 4px}} .sub{{color:var(--muted);margin-bottom:16px}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:20px}}
.tile{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}}
.n{{font-size:26px;font-weight:650;color:var(--accent);font-variant-numeric:tabular-nums}} .l{{color:var(--muted);font-size:12px}}
.wrap{{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px;margin-bottom:20px}}
table{{border-collapse:collapse;width:100%;min-width:900px}} th,td{{padding:8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
th{{font-size:12px;color:var(--muted);position:sticky;top:0;background:var(--card)}} small{{color:var(--muted)}} a{{color:var(--accent)}}
input{{padding:8px;width:100%;max-width:360px;margin-bottom:10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg)}}
</style></head><body>
<h1>Internship Hunt — December 2026</h1><div class="sub">Generated {today} from companies.csv and applications.csv</div>
<div class="tiles">{tiles}</div>
<h2>Applications</h2><div class="wrap"><table><tr><th>Company</th><th>To</th><th>Subject</th><th>Status</th><th>Sent</th><th>Follow-up 1</th><th>Reply</th></tr>{arow}</table></div>
<h2>Companies (by priority)</h2><input id="q" placeholder="Filter…" oninput="f(this.value)">
<div class="wrap"><table id="c"><tr><th>Score</th><th>Company</th><th>Role</th><th>Location</th><th>Pay</th><th>Urgency</th><th>Dec start</th><th>Contact</th><th>Status</th><th></th></tr>{crow}</table></div>
<script>function f(q){{q=q.toLowerCase();document.querySelectorAll('#c tr:not(:first-child)').forEach(r=>r.style.display=r.textContent.toLowerCase().includes(q)?'':'none')}}</script>
</body></html>""", encoding="utf-8")
    print(f"wrote {DASHBOARD.name}")


def sources():
    """Write research_sources.md: every company's evidence and source links, by priority."""
    comps = read_csv(COMPANIES, COMPANY_FIELDS)
    out = [
        "# Research sources and notes",
        "",
        "Generated from `companies.csv`. Each entry lists the evidence and the URLs it came from.",
        "**Verification caveat (2026-10-11):** this environment's network policy blocked direct page loads,",
        "so facts were taken from web-search result text for these URLs, not from reading the pages.",
        "Open each source and confirm the posting is live before applying or emailing.",
        "",
    ]
    for c in comps:
        out += [
            f"## {c['id']} · {c['company']} — score {c['priority_score']}",
            f"- **Role:** {c['best_fit_role']} ({c['vacancy_type']}) · {c['location']} · {c['work_mode']}",
            f"- **Pay:** {c['paid_status']} {('— ' + c['stipend']) if c['stipend'] else ''} · **Duration:** {c['duration'] or 'n/a'}",
            f"- **Hiring urgency:** {c['hiring_urgency']} — {c['urgency_reason']}",
            f"- **Evidence:** {c['hiring_evidence']}",
            f"- **December start:** {c['december_start']}",
            f"- **Contact:** {c['contact_name'] or '—'} {('(' + c['contact_title'] + ')') if c['contact_title'] else ''} · "
            f"{c['contact_email'] or 'NOT FOUND'} · {c['email_status']} {c['email_source']}",
            f"- **Careers / LinkedIn:** {c['linkedin_or_careers_url'] or '—'}",
            f"- **Sources (checked {c['date_checked']}):** " + " ".join(f"<{u}>" for u in dict.fromkeys(c["source_urls"].split())),
        ]
        if c["notes"]:
            out.append(f"- **Notes:** {c['notes']}")
        out.append("")
    (HERE / "research_sources.md").write_text("\n".join(out), encoding="utf-8")
    print("wrote research_sources.md")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dashboard"
    if cmd == "merge":
        merge(sys.argv[2:])
    elif cmd == "score":
        rescore()
    elif cmd == "sources":
        sources()
    elif cmd == "followups":
        followups()
    else:
        dashboard()
