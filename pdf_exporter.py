from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

def create_exam_pdf(quiz_data) -> io.BytesIO:
    """Generates a PDF exam and answer key from the quiz data using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = 1 # Center alignment
    
    question_style = styles['Normal']
    question_style.fontName = 'Helvetica-Bold'
    question_style.spaceAfter = 6
    question_style.fontSize = 11
    
    normal_style = styles['Normal']
    normal_style.spaceAfter = 12
    normal_style.fontSize = 11
    
    answer_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        textColor=colors.darkgreen,
        spaceAfter=6,
        fontSize=11,
        fontName='Helvetica-Bold'
    )
    
    explanation_style = ParagraphStyle(
        'ExplanationStyle',
        parent=styles['Normal'],
        textColor=colors.dimgrey,
        spaceAfter=12,
        leftIndent=20,
        fontSize=10,
        fontName='Helvetica-Oblique'
    )

    Story = []

    # --- EXAM SECTION ---
    Story.append(Paragraph("AI Generated Exam", title_style))
    Story.append(Spacer(1, 24))
    
    for i, q in enumerate(quiz_data.questions, 1):
        Story.append(Paragraph(f"{i}. {q.question_text}", question_style))
        
        if q.type == "mcq" and q.options:
            for j, opt in enumerate(q.options):
                letter_choice = chr(65 + j) # A, B, C, D
                Story.append(Paragraph(f"   {letter_choice}) {opt}", normal_style))
        elif q.type == "true_false":
            Story.append(Paragraph("   [  ] True", normal_style))
            Story.append(Paragraph("   [  ] False", normal_style))
        else:
            # Short answer space
            Story.append(Spacer(1, 48))
            Story.append(Paragraph("_" * 60, normal_style))
            Story.append(Spacer(1, 12))
    
    # Page Break for Answer Key
    Story.append(PageBreak())
    
    # --- ANSWER KEY SECTION ---
    Story.append(Paragraph("Answer Key & Explanations", title_style))
    Story.append(Spacer(1, 24))
    
    for i, q in enumerate(quiz_data.questions, 1):
        Story.append(Paragraph(f"{i}. {q.question_text}", question_style))
        Story.append(Paragraph(f"Correct Answer: {q.correct_answer}", answer_style))
        Story.append(Paragraph(f"Explanation: {q.explanation}", explanation_style))

    doc.build(Story)
    buffer.seek(0)
    return buffer
