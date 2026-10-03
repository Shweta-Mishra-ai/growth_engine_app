"""
services/pdf_export.py — High-quality PDF export with proper typography,
color coding per platform, and professional layout using ReportLab.
"""
from __future__ import annotations
import io
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
        Table, TableStyle, KeepTogether,
    )
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False
    colors = None
    letter = None

# ── Color palette ────────────────────────────────────────
if HAS_REPORTLAB:
    C_ACCENT   = colors.HexColor("#6366f1")   # brand purple
    C_DARK     = colors.HexColor("#1e2330")   # dark bg
    C_MUTED    = colors.HexColor("#64748b")   # muted text
    C_BORDER   = colors.HexColor("#e2e8f0")   # border
    C_LI_BLUE  = colors.HexColor("#0a66c2")   # LinkedIn
    C_TW_BLACK = colors.HexColor("#000000")   # Twitter/X
    C_IG_PINK  = colors.HexColor("#e1306c")   # Instagram
    C_HOOKS    = colors.HexColor("#f59e0b")   # hooks/gold
    C_VOICE    = colors.HexColor("#10b981")   # voice DNA

    PLATFORM_COLORS = {
        "LinkedIn":        C_LI_BLUE,
        "Twitter/X":       C_TW_BLACK,
        "Instagram":       C_IG_PINK,
        "Hooks":           C_HOOKS,
        "Voice DNA":       C_VOICE,
        "Voice-Matched":   C_VOICE,
        "Post Autopsy":    C_ACCENT,
        "Pattern-Applied": C_ACCENT,
    }


def _styles():
    if not HAS_REPORTLAB:
        return None, None, None, None, None, None
    base = getSampleStyleSheet()

    title = ParagraphStyle(
        "GETitle",
        parent=base["Title"],
        fontSize=24,
        fontName="Helvetica-Bold",
        textColor=C_DARK,
        spaceAfter=4,
        leading=28,
    )
    subtitle = ParagraphStyle(
        "GESubtitle",
        parent=base["Normal"],
        fontSize=9,
        fontName="Helvetica",
        textColor=C_MUTED,
        spaceAfter=16,
    )
    entry_type = ParagraphStyle(
        "EntryType",
        parent=base["Normal"],
        fontSize=8,
        fontName="Helvetica-Bold",
        textColor=colors.white,
        spaceAfter=0,
        leftIndent=6,
    )
    entry_meta = ParagraphStyle(
        "EntryMeta",
        parent=base["Normal"],
        fontSize=8,
        fontName="Helvetica",
        textColor=C_MUTED,
        spaceAfter=6,
    )
    body = ParagraphStyle(
        "EntryBody",
        parent=base["Normal"],
        fontSize=10,
        fontName="Helvetica",
        leading=15,
        spaceAfter=0,
        textColor=C_DARK,
    )
    footer_style = ParagraphStyle(
        "Footer",
        parent=base["Normal"],
        fontSize=8,
        fontName="Helvetica",
        textColor=C_MUTED,
        alignment=TA_CENTER,
    )
    return title, subtitle, entry_type, entry_meta, body, footer_style


def build_content_pdf(
    entries: list,
    title: str = "Growth Engine AI — Content Export",
    page_size=None,
) -> bytes:
    """
    Build a polished, professionally designed PDF from history entries.
    Returns raw PDF bytes.
    """
    if not HAS_REPORTLAB:
        raise ImportError("ReportLab is not installed.")

    if page_size is None:
        page_size = letter

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=page_size,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        title=title,
        author="Growth Engine AI",
        subject="Social Media Content Export",
    )

    s_title, s_subtitle, s_entry_type, s_meta, s_body, s_footer = _styles()
    story = []

    # ── Cover header ─────────────────────────────────────
    story.append(Paragraph("🚀 Growth Engine AI", s_title))
    story.append(Paragraph(
        f"Content Export &nbsp;·&nbsp; "
        f"Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')} &nbsp;·&nbsp; "
        f"{len(entries)} item{'s' if len(entries) != 1 else ''}",
        s_subtitle,
    ))
    story.append(HRFlowable(
        width="100%", thickness=2,
        color=C_ACCENT, spaceAfter=18,
    ))

    if not entries:
        story.append(Paragraph("No content to export.", s_meta))
        doc.build(story)
        buf.seek(0)
        return buf.read()

    # ── Entries ───────────────────────────────────────────
    for idx, entry in enumerate(entries, 1):
        entry_type = entry.get("type", "Content")
        platform   = entry.get("platform", "")
        content    = entry.get("content", "")
        timestamp  = entry.get("timestamp", "")

        platform_color = PLATFORM_COLORS.get(platform, C_ACCENT)
        for key in PLATFORM_COLORS:
            if key.lower() in entry_type.lower():
                platform_color = PLATFORM_COLORS[key]
                break

        # Badge
        badge_label = f"{idx}. {entry_type}" + (f"  ·  {platform}" if platform else "")
        badge_data  = [[Paragraph(badge_label, s_entry_type)]]
        badge_table = Table(badge_data, colWidths=["100%"])
        badge_table.setStyle(TableStyle([
            ("BACKGROUND",  (0, 0), (-1, -1), platform_color),
            ("ROUNDEDCORNERS", [6, 6, 0, 0]),
            ("TOPPADDING",  (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]))

        # Meta
        meta_parts = []
        if timestamp:
            meta_parts.append(timestamp)
        meta_text = "  ·  ".join(meta_parts) if meta_parts else ""

        # Content
        display_content = content[:2000] + ("\n\n[... truncated for PDF ...]" if len(content) > 2000 else "")
        safe_content = (
            display_content
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br/>")
        )
        content_para = Paragraph(safe_content, s_body)
        content_data = [[content_para]]
        content_table = Table(content_data, colWidths=["100%"])
        content_table.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX",          (0, 0), (-1, -1), 1, C_BORDER),
            ("TOPPADDING",   (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 12),
            ("LEFTPADDING",  (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("ROUNDEDCORNERS", [0, 0, 6, 6]),
        ]))

        block = [badge_table]
        if meta_text:
            block.append(Paragraph(meta_text, s_meta))
        block.append(content_table)
        block.append(Spacer(1, 14))

        story.append(KeepTogether(block))

    # ── Footer ────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceBefore=8, spaceAfter=6))
    story.append(Paragraph(
        f"Generated by Growth Engine AI v3.1 &nbsp;·&nbsp; {datetime.now().strftime('%Y-%m-%d')}",
        s_footer,
    ))

    doc.build(story)
    buf.seek(0)
    return buf.read()
