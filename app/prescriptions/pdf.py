from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_prescription_pdf(prescription):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('title', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=16)
    subtitle_style = ParagraphStyle('subtitle', parent=styles['Normal'], alignment=TA_CENTER, fontSize=11)
    normal_style = styles['Normal']
    bold_style = ParagraphStyle('bold', parent=styles['Normal'], fontName='Helvetica-Bold')

    story = []

    # Başlık
    story.append(Paragraph('RECETE', title_style))
    story.append(Spacer(1, 0.3*cm))

    doctor = prescription.doctor
    doctor_name = f'{doctor.title} {doctor.user.get_full_name()}'.strip()
    branch = str(doctor.branch) if doctor.branch else ''
    story.append(Paragraph(f'{doctor_name}  {branch}', subtitle_style))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.black))
    story.append(Spacer(1, 0.5*cm))

    # Hasta Bilgisi
    patient = prescription.patient
    story.append(Paragraph(f'<b>Hasta:</b> {patient.full_name}', normal_style))
    if patient.birth_date:
        story.append(Paragraph(f'<b>Doğum Tarihi:</b> {patient.birth_date:%d.%m.%Y}', normal_style))
    story.append(Paragraph(f'<b>Tarih:</b> {prescription.prescription_date:%d.%m.%Y}', normal_style))
    story.append(Spacer(1, 0.5*cm))

    # İlaçlar
    story.append(Paragraph('<b>İlaçlar:</b>', bold_style))
    story.append(Spacer(1, 0.2*cm))

    for i, item in enumerate(prescription.items.all(), 1):
        story.append(Paragraph(
            f'{i}. <b>{item.medicine_name}</b> - {item.dosage}',
            normal_style
        ))
        detail = []
        if item.frequency:
            detail.append(f'Kullanım: {item.frequency}')
        if item.duration:
            detail.append(f'Süre: {item.duration}')
        if detail:
            story.append(Paragraph(f'&nbsp;&nbsp;&nbsp;{" | ".join(detail)}', normal_style))
        if item.usage_instruction:
            story.append(Paragraph(f'&nbsp;&nbsp;&nbsp;Talimat: {item.usage_instruction}', normal_style))
        story.append(Spacer(1, 0.2*cm))

    if prescription.note:
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph(f'<b>Not:</b> {prescription.note}', normal_style))

    story.append(Spacer(1, 1.5*cm))
    story.append(HRFlowable(width='50%', thickness=1, color=colors.black))
    story.append(Paragraph(f'{doctor_name}', normal_style))
    story.append(Paragraph('Doktor İmzası / Kaşe', normal_style))

    doc.build(story)
    return buffer.getvalue()
