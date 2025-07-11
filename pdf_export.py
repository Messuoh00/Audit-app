import io
import os
import plotly.express as px
import plotly.io as pio
import pandas as pd
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def export_pdf(session):
    pdf_buffer = io.BytesIO()
    styles = getSampleStyleSheet()
    elements = []

    # Header
    elements.append(Paragraph("Cybersecurity Assessment Report", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Organization: {session['org']}", styles['Normal']))
    elements.append(Paragraph(f"Assessor: {session['assessor']}", styles['Normal']))
    elements.append(Paragraph(f"Date: {session['date']}", styles['Normal']))
    elements.append(Spacer(1, 24))

    # DataFrame
    df = pd.DataFrame([
        {**q, "Answer": a["answer"], "Note": a["note"], "Evidence": os.path.basename(ev) if ev else ""}
        for q, a, ev in zip(session["questionnaire"], session["answers"], session["evidence"])
    ])
    score = df["Answer"].map({"Yes": 2, "Partial": 1, "No": 0}).sum()
    max_score = len(df) * 2
    percent = round(100 * score / max_score, 1) if max_score > 0 else 0
    maturity = (
        "Mature" if percent >= 67 else
        "Developing" if percent >= 34 else
        "Initial"
    )
    elements.append(Paragraph(f"Compliance Score: {score}/{max_score} ({percent}%)", styles['Heading2']))
    elements.append(Paragraph(f"Maturity Level: {maturity}", styles['Heading3']))
    elements.append(Spacer(1, 12))

    # Chart 1: Compliance by Domain
    by_domain = df.groupby("Domain")["Answer"].apply(lambda x: (x == "Yes").sum() / len(x) * 100 if len(x) > 0 else 0)
    fig = px.bar(by_domain, labels={"value": "Compliance %"}, title="Compliance by Domain")
    img_bytes = io.BytesIO()
    pio.write_image(fig, img_bytes, format="png", width=700, height=400, scale=2)
    img_bytes.seek(0)
    elements.append(RLImage(img_bytes, width=400, height=220))
    elements.append(Spacer(1, 16))

    # Chart 2: Maturity Radar
    maturity_scores = {'Initial': 1, 'Repeatable': 2, 'Defined': 3, 'Managed': 4, 'Optimizing': 5}
    domain_maturity = session["domain_maturity"]
    radar_df = pd.DataFrame([{"Domain": d, "Maturity": maturity_scores.get(domain_maturity.get(d, "Initial"), 1)} for d in domain_maturity])
    if not radar_df.empty:
        radar = px.line_polar(radar_df, r='Maturity', theta='Domain', line_close=True, title="Maturity by Domain", range_r=[1, 5])
        radar_bytes = io.BytesIO()
        pio.write_image(radar, radar_bytes, format="png", width=500, height=400, scale=2)
        radar_bytes.seek(0)
        elements.append(RLImage(radar_bytes, width=350, height=250))
        elements.append(Spacer(1, 16))

    # Gap Table
    elements.append(Paragraph("Gap Analysis", styles['Heading2']))
    gap_df = df[df["Answer"].isin(["Partial", "No"])]
    if not gap_df.empty:
        gap_data = [list(gap_df.columns)] + gap_df.values.tolist()
        col_widths = [80, 60, 80, 45, 120, 90, 65]
        def wrap(text):
            from reportlab.platypus import Paragraph
            return Paragraph(str(text), styles['Normal'])
        gap_data_wrapped = [
            [wrap(val) for val in row]
            for row in gap_data
        ]
        table = Table(gap_data_wrapped, repeatRows=1, colWidths=col_widths)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#fbeaea")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 16))
    else:
        elements.append(Paragraph("No gaps found.", styles['Normal']))
        elements.append(Spacer(1, 16))

    # Evidence List
    elements.append(Paragraph("Evidence Files", styles['Heading3']))
    evidence_files = [os.path.basename(ev) for ev in session["evidence"] if ev]
    if evidence_files:
        for f in evidence_files:
            elements.append(Paragraph(f"- {f}", styles['Normal']))
    else:
        elements.append(Paragraph("No evidence uploaded.", styles['Normal']))

    # Build PDF in-memory and download
    doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4))
    doc.build(elements)
    pdf_buffer.seek(0)
    from nicegui import ui
    ui.notify("PDF report generated. Download will start.")
    ui.download(pdf_buffer.getvalue(), filename="assessment_report.pdf")
