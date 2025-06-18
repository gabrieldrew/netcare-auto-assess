import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import HRFlowable


def generate_assessment_pdf(claim_data, result, claim_form_data):
    """Generate a PDF report of the claim assessment."""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#1D3443'),
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#1D3443'),
        leftIndent=0
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        textColor=colors.HexColor('#1D3443')
    )
    
    # Title
    elements.append(Paragraph("NetcarePlus GapCare", title_style))
    elements.append(Paragraph("Claim Assessment Report", title_style))
    elements.append(Spacer(1, 20))
    
    # Report Details
    report_data = [
        ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        ['Assessment Status:', 'COVERED' if result.get('covered') else 'NOT COVERED'],
    ]
    
    if claim_form_data.get('policy_number'):
        report_data.append(['Policy Number:', claim_form_data.get('policy_number', 'N/A')])
    
    if claim_form_data.get('policyholder_name') and claim_form_data.get('policyholder_surname'):
        report_data.append(['Policyholder:', f"{claim_form_data.get('policyholder_name', '')} {claim_form_data.get('policyholder_surname', '')}"])
    
    report_table = Table(report_data, colWidths=[2*inch, 4*inch])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D0E9F3')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1D3443')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#22D3EE')),
    ]))
    
    elements.append(report_table)
    elements.append(Spacer(1, 20))
    
    # Assessment Result
    elements.append(Paragraph("Assessment Result", heading_style))
    elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor('#22D3EE')))
    elements.append(Spacer(1, 10))
    
    # Coverage Status
    coverage_text = "CLAIM COVERED" if result.get('covered') else "CLAIM NOT COVERED"
    coverage_color = colors.HexColor('#059669') if result.get('covered') else colors.HexColor('#DC2626')
    coverage_style = ParagraphStyle(
        'CoverageStyle',
        parent=normal_style,
        fontSize=14,
        textColor=coverage_color,
        alignment=1,
        fontName='Helvetica-Bold'
    )
    elements.append(Paragraph(coverage_text, coverage_style))
    elements.append(Spacer(1, 15))
    
    # Applicable Benefits
    if result.get('benefits'):
        elements.append(Paragraph("Applicable Benefits", heading_style))
        for benefit in result['benefits']:
            elements.append(Paragraph(f"• {benefit}", normal_style))
        elements.append(Spacer(1, 15))
    
    # Payable Amount
    if result.get('payable_amount_ZAR'):
        elements.append(Paragraph("Financial Assessment", heading_style))
        amount_style = ParagraphStyle(
            'AmountStyle',
            parent=normal_style,
            fontSize=13,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#059669')
        )
        elements.append(Paragraph(f"Estimated Payable Amount: {result['payable_amount_ZAR']}", amount_style))
        elements.append(Spacer(1, 15))
    
    # Explanation
    elements.append(Paragraph("Detailed Explanation", heading_style))
    elements.append(Paragraph(result.get('explanation', 'No explanation provided'), normal_style))
    elements.append(Spacer(1, 20))
    
    # Patient Information (if available)
    if claim_form_data.get('patient_name') or claim_form_data.get('patient_surname'):
        elements.append(Paragraph("Patient Information", heading_style))
        elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor('#22D3EE')))
        elements.append(Spacer(1, 10))
        
        patient_data = []
        if claim_form_data.get('patient_name') and claim_form_data.get('patient_surname'):
            patient_data.append(['Patient Name:', f"{claim_form_data.get('patient_name', '')} {claim_form_data.get('patient_surname', '')}"])
        
        if claim_form_data.get('patient_id'):
            patient_data.append(['Patient ID:', claim_form_data.get('patient_id', 'N/A')])
        
        if claim_form_data.get('relationship'):
            patient_data.append(['Relationship:', claim_form_data.get('relationship', 'N/A')])
        
        if claim_form_data.get('admission_date'):
            patient_data.append(['Admission Date:', claim_form_data.get('admission_date', 'N/A')])
        
        if patient_data:
            patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
            patient_table.setStyle(TableStyle([
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1D3443')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D0E9F3')),
            ]))
            elements.append(patient_table)
            elements.append(Spacer(1, 20))
    
    # Medical Aid Information
    if claim_form_data.get('medical_aid'):
        elements.append(Paragraph("Medical Aid Information", heading_style))
        elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.HexColor('#22D3EE')))
        elements.append(Spacer(1, 10))
        
        medical_data = [
            ['Medical Aid:', claim_form_data.get('medical_aid', 'N/A')],
            ['Option:', claim_form_data.get('option', 'N/A')]
        ]
        
        medical_table = Table(medical_data, colWidths=[2*inch, 4*inch])
        medical_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1D3443')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D0E9F3')),
        ]))
        elements.append(medical_table)
        elements.append(Spacer(1, 30))
    
    # Footer disclaimer
    disclaimer_style = ParagraphStyle(
        'DisclaimerStyle',
        parent=normal_style,
        fontSize=9,
        textColor=colors.HexColor('#64748B'),
        alignment=1
    )
    elements.append(Paragraph("DEMO ASSESSMENT ONLY - HUMAN AUDIT REQUIRED BEFORE PAYMENT", disclaimer_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("This assessment is generated by an AI system and should be reviewed by a qualified claims assessor.", disclaimer_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer