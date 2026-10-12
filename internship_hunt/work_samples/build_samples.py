"""Rebuild Wrick's two work-sample PDFs (text taken from his originals; CAPS role line aligned with resume)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ACC = colors.HexColor("#0f766e")
S = {
    "kick": ParagraphStyle("k", fontName="Helvetica-Bold", fontSize=8, textColor=ACC, spaceAfter=4),
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=18, leading=22, spaceAfter=4),
    "sub": ParagraphStyle("s", fontName="Helvetica", fontSize=9.5, textColor=colors.HexColor("#555555"), spaceAfter=10),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.5, spaceBefore=10, spaceAfter=4, textColor=ACC),
    "p": ParagraphStyle("p", fontName="Helvetica", fontSize=9.3, leading=13),
    "b": ParagraphStyle("b", fontName="Helvetica", fontSize=9.3, leading=13, leftIndent=10, bulletIndent=0, spaceAfter=2),
    "n": ParagraphStyle("n", fontName="Helvetica-Bold", fontSize=16, alignment=1, textColor=ACC),
    "nl": ParagraphStyle("nl", fontName="Helvetica", fontSize=8, alignment=1, textColor=colors.HexColor("#555555")),
}


def footer(c, d):
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#777777"))
    c.drawString(18 * mm, 10 * mm, "WRICK MAJUMDAR | SELECTED WORK")
    c.drawRightString(A4[0] - 18 * mm, 10 * mm, str(d.page))


def stats(items):
    t = Table([[Paragraph(n, S["n"]) for n, _ in items], [Paragraph(l, S["nl"]) for _, l in items]],
              colWidths=[(A4[0] - 36 * mm) / len(items)] * len(items))
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                           ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f4faf9")),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def bullets(lst):
    return [Paragraph(f"<b>{h}:</b> {t}" if h else t, S["b"], bulletText="•") for h, t in lst]


def build(path, story):
    SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                      bottomMargin=16 * mm, title="Wrick Majumdar - Work Sample", author="Wrick Majumdar"
                      ).build(story, onFirstPage=footer, onLaterPages=footer)


ai = [
    Paragraph("WORK SAMPLE 01 / GROWTH · CONTENT · RESEARCH", S["kick"]),
    Paragraph("AI Tool Testing &amp; Research", S["h1"]),
    Paragraph("Selected work across hands-on product evaluation, AI-tool landscape research, and founder outreach.", S["sub"]),
    Paragraph("Overview", S["h2"]),
    Paragraph("Through my work with AIDemos, I researched AI products, explored their practical use cases, tested product "
              "workflows, and supported outreach to tool teams. My approach combines curiosity about new products with "
              "structured testing, clear evidence, and concise communication of what works, what does not, and what needs "
              "further verification.", S["p"]),
    Spacer(1, 8),
    stats([("13", "MarkItDown test cases executed"), ("3", "Research focus areas"), ("1", "Tool team providing premium access")]),
    Paragraph("Case study: MarkItDown PDF-to-Markdown testing", S["h2"]),
    Paragraph("<b>Objective.</b> Evaluate how reliably a document-conversion workflow handled a set of PDF test cases, "
              "while keeping the results traceable to evidence.", S["p"]),
    Spacer(1, 4),
    *bullets([
        ("Execution", "Ran 13 test cases and captured supporting PDFs, screenshots, Markdown outputs, logs, and other evidence."),
        ("Observed outcome", "1 test passed, 6 failed, and 6 could not be graded."),
        ("Important limitation", "The ungradable cases were blocked by a ClickUp CDN/egress 403 issue, so those cases were "
                                 "recorded as blocked rather than treated as product failures."),
        ("Research habit", "Separate confirmed failures from infrastructure blockers; preserve evidence so another reviewer "
                           "can reproduce or audit the outcome."),
    ]),
    Paragraph("AI product research &amp; outreach", S["h2"]),
    *bullets([
        ("Landscape research", "Explored tools across AI lead discovery, email finding and verification, web scraping and "
                               "enrichment, cold-email personalization, outreach automation, and AI SDR workflows."),
        ("Product discovery", "Reviewed product positioning and practical use cases to identify which tools could be relevant "
                              "to AIDemos’ audience."),
        ("Founder/team outreach", "Supported personalized outreach to AI product teams, including requests for product access "
                                  "and potential review or collaboration opportunities."),
        ("Access &amp; follow-through", "Secured premium access from Firecrawl, enabling deeper product exploration."),
    ]),
    Paragraph("What this demonstrates", S["h2"]),
    *bullets([
        ("Research", "Landscape mapping, use-case discovery, product comparison."),
        ("Testing", "Test execution, evidence capture, issue classification."),
        ("Content thinking", "Turning product exploration into clear, audience-relevant insights."),
        ("Growth support", "Personalized outreach, access requests, relationship follow-up."),
    ]),
    Spacer(1, 6),
    Paragraph("<b>Working principle:</b> I aim to make product research useful to a real audience—test carefully, distinguish "
              "evidence from assumptions, and communicate findings in a way that supports content decisions and growth.", S["p"]),
]

caps = [
    Paragraph("WORK SAMPLE 02 / LEADERSHIP · COORDINATION · EXECUTION", S["kick"]),
    Paragraph("Leadership &amp; Event Operations", S["h1"]),
    Paragraph("Selected experience with the Centre for Academic and Professional Support (CAPS), Christ University.", S["sub"]),
    Paragraph("My role", S["h2"]),
    Paragraph("I am a Member and Content Lead at CAPS, where I lead media promotion and public relations, and I also work "
              "with the CAPS Operations Wing. This experience focused on supporting student initiatives through planning, "
              "coordination, and practical event operations—helping activities run smoothly for speakers, participants, "
              "and volunteers.", S["p"]),
    Paragraph("Operations in practice", S["h2"]),
    *bullets([
        ("Planning &amp; logistics", "Helped coordinate event requirements, schedules, venue readiness, and the details needed "
                                     "for a smooth participant experience."),
        ("Volunteer coordination", "Worked across responsibilities and supported clear task allocation so that event-day "
                                   "execution stayed organized."),
        ("Participant experience", "Supported registration, guest hospitality, audience flow, and on-the-ground issue resolution."),
        ("Cross-functional execution", "Coordinated practical requirements such as stage and technical setup, food and "
                                       "beverage arrangements, signage, and post-event feedback where needed."),
    ]),
    Paragraph("Example: Professional Lecture Series &amp; Networking Luncheon", S["h2"]),
    Paragraph("A university event-operations example involved a programme planned for approximately 200 attendees, supported "
              "by a team of around 15 volunteers. The operational checklist covered registration, stage and audience "
              "management, technical coordination, hospitality, catering, signage, and feedback collection. The planning "
              "notes included an estimated budget of Rs 15,000.", S["p"]),
    Spacer(1, 8),
    stats([("~200", "Expected attendees"), ("~15", "Volunteers"), ("Rs 15,000", "Estimated event budget")]),
    Paragraph("Leadership strengths", S["h2"]),
    *bullets([
        ("Ownership", "Pay attention to operational details before they become event-day problems."),
        ("Communication", "Keep participants, volunteers, and stakeholders aligned on practical requirements."),
        ("Adaptability", "Respond to changing needs while keeping the attendee experience in view."),
        ("Team-first mindset", "Help different workstreams come together toward one shared outcome."),
    ]),
    Paragraph("How this connects to a Growth / Content &amp; Research role", S["h2"]),
    Paragraph("The same habits carry into growth and research work: organize moving pieces, follow through on commitments, "
              "understand the audience, communicate clearly, and turn a broad goal into a practical checklist. I enjoy work "
              "that sits at the intersection of people, information, and execution.", S["p"]),
    Spacer(1, 6),
    Paragraph("<b>Core takeaway:</b> I bring hands-on coordination experience, attention to detail, and a bias toward getting "
              "work done collaboratively.", S["p"]),
]

if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    build(os.path.join(here, "Wrick_Majumdar_AI_Tool_Testing_Research.pdf"), ai)
    build(os.path.join(here, "Wrick_Majumdar_CAPS_Leadership.pdf"), caps)
    print("built")
