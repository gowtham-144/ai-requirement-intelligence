from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def generate_pdf(report, filename="requirement_report.pdf"):

    doc = SimpleDocTemplate(filename)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("AI Requirement Intelligence Report", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Executive Summary", styles["Heading2"]))
    elements.append(Paragraph(report["executive_summary"], styles["BodyText"]))
    elements.append(Spacer(1, 0.3 * inch))

    sections = [
        ("Functional Requirements", report["functional_requirements"]),
        ("Non-Functional Requirements", report["non_functional_requirements"]),
        ("Ambiguities", report["ambiguities"]),
        ("Technical Risks", report["technical_risks"]),
        ("Improvements", report["improvements"]),
    ]

    for title, items in sections:
        elements.append(Paragraph(title, styles["Heading2"]))
        elements.append(Spacer(1, 0.1 * inch))
        elements.append(
            ListFlowable(
                [ListItem(Paragraph(i, styles["BodyText"])) for i in items],
                bulletType='bullet'
            )
        )
        elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Final Clarity Score", styles["Heading2"]))
    elements.append(Paragraph(str(report["final_score"]) + " / 100", styles["BodyText"]))

    doc.build(elements)

    return filename
