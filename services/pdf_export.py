import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable


def build_content_pdf(entries: list, title: str = "Growth Engine AI — Content Export") -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch,
                             leftMargin=0.75*inch, rightMargin=0.75*inch)
    styles = getSampleStyleSheet()
    ts = ParagraphStyle("T", parent=styles["Title"], fontSize=20, spaceAfter=6, textColor=colors.HexColor("#1e2330"))
    ms = ParagraphStyle("M", parent=styles["Normal"], fontSize=9, textColor=colors.HexColor("#64748b"), spaceAfter=20)
    hs = ParagraphStyle("H", parent=styles["Heading2"], fontSize=13, spaceAfter=8, textColor=colors.HexColor("#6366f1"))
    bs = ParagraphStyle("B", parent=styles["Normal"], fontSize=10.5, leading=16, spaceAfter=16)

    story = [Paragraph(title, ts),
             Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", ms),
             HRFlowable(width="100%", color=colors.HexColor("#e2e8f0"), thickness=1),
             Spacer(1, 16)]

    for i, e in enumerate(entries, 1):
        hdr = f"{i}. {e.get('type','Content')}" + (f" — {e.get('platform','')}" if e.get('platform') else "")
        story.append(Paragraph(hdr, hs))
        if e.get("timestamp"):
            story.append(Paragraph(e["timestamp"], ms))
        safe = e.get("content","").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>")
        story.append(Paragraph(safe, bs))
        story.append(HRFlowable(width="100%", color=colors.HexColor("#e2e8f0"), thickness=0.5))
        story.append(Spacer(1, 16))

    doc.build(story)
    buf.seek(0)
    return buf.read()
