from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from results.services import calculate_gpa, calculate_cgpa, get_academic_standing


def generate_result_slip_pdf(student, session, semester, results):
    """
    Generates a single-semester result slip for one student.
    Returns a BytesIO buffer ready to be served as an HTTP response.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Heading1"], alignment=1, fontSize=16
    )
    subtitle_style = ParagraphStyle(
        "SubtitleStyle", parent=styles["Normal"], alignment=1, fontSize=10, textColor=colors.grey
    )

    elements = []
    elements.append(Paragraph("STUDENT RESULT SLIP", title_style))
    elements.append(Paragraph(f"{session.name} - {semester.get_name_display()}", subtitle_style))
    elements.append(Spacer(1, 0.5*cm))

    # student info block
    info_data = [
        ["Name:", student.full_name, "Matric No:", student.matric_number],
        ["Department:", student.department.name if student.department else "-",
         "Level:", f"{student.level}" if student.level else "-"],
    ]
    info_table = Table(info_data, colWidths=[3*cm, 6*cm, 3*cm, 5*cm])
    info_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.7*cm))

    # results table
    table_data = [["Course Code", "Course Title", "Unit", "Score", "Grade", "Grade Point"]]
    for r in results:
        table_data.append([
            r.course.code,
            r.course.title,
            str(r.course.unit),
            str(r.total_score),
            r.grade,
            str(r.grade_point),
        ])

    results_table = Table(table_data, colWidths=[2.5*cm, 6*cm, 1.5*cm, 2*cm, 1.8*cm, 2.7*cm])
    results_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (2, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
    ]))
    elements.append(results_table)
    elements.append(Spacer(1, 0.7*cm))

    # GPA summary
    gpa = calculate_gpa(student, session, semester)
    cgpa = calculate_cgpa(student)
    standing = get_academic_standing(cgpa)

    summary_data = [
        ["Semester GPA:", str(gpa)],
        ["Cumulative CGPA:", str(cgpa)],
        ["Academic Standing:", standing],
    ]
    summary_table = Table(summary_data, colWidths=[5*cm, 6*cm])
    summary_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(summary_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_transcript_pdf(student, all_results_by_semester):
    """
    Generates a full transcript across all sessions/semesters.
    all_results_by_semester: list of dicts like
        [{"session": Session, "semester": Semester, "results": [Result, ...]}, ...]
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("TitleStyle", parent=styles["Heading1"], alignment=1, fontSize=16)
    section_style = ParagraphStyle("SectionStyle", parent=styles["Heading3"], fontSize=11, spaceBefore=10)

    elements = []
    elements.append(Paragraph("ACADEMIC TRANSCRIPT", title_style))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph(f"{student.full_name} ({student.matric_number})", styles["Normal"]))
    elements.append(Paragraph(f"{student.department} - {student.programme} {student.level}", styles["Normal"]))
    elements.append(Spacer(1, 0.5*cm))

    for block in all_results_by_semester:
        session = block["session"]
        semester = block["semester"]
        results = block["results"]

        elements.append(Paragraph(f"{session.name} - {semester.get_name_display()}", section_style))

        table_data = [["Course", "Title", "Unit", "Score", "Grade", "GP"]]
        for r in results:
            table_data.append([r.course.code, r.course.title, str(r.course.unit),
                                str(r.total_score), r.grade, str(r.grade_point)])

        table = Table(table_data, colWidths=[2.2*cm, 6*cm, 1.3*cm, 1.8*cm, 1.5*cm, 1.5*cm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#34495e")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ]))
        elements.append(table)

        gpa = calculate_gpa(student, session, semester)
        elements.append(Paragraph(f"Semester GPA: {gpa}", styles["Normal"]))
        elements.append(Spacer(1, 0.4*cm))

    cgpa = calculate_cgpa(student)
    standing = get_academic_standing(cgpa)
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph(f"<b>Cumulative CGPA: {cgpa}</b>", styles["Normal"]))
    elements.append(Paragraph(f"<b>Academic Standing: {standing}</b>", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer







