import csv
import tempfile
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from app.utils import get_question_text, get_maturity_level

def generate_pdf_report(assessment, system):
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    doc = SimpleDocTemplate(tmp.name, pagesize=letter)
    styles = getSampleStyleSheet()
    el = []

    # Get maturity level info
    level_num, level_name, _ = get_maturity_level(assessment.overall_score)

    el += [
        Paragraph("Legacy System Maturity Assessment Report", styles["Title"]),
        Paragraph(f"System: {system.name}", styles["Heading1"]),
        Paragraph(
            f"Date: {assessment.timestamp.strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"],
        ),
        Spacer(1, 18),
        Paragraph(
            f"Overall Maturity Score: {assessment.overall_score:.1f}/100 (Level {level_num}: {level_name})",
            styles["Heading2"],
        ),
        Spacer(1, 18),
    ]

    # Get maturity levels for each dimension
    sec_level, sec_name, _ = get_maturity_level(assessment.security_score)
    fin_level, fin_name, _ = get_maturity_level(assessment.financial_score)
    op_level, op_name, _ = get_maturity_level(assessment.operational_score)
    gov_level, gov_name, _ = get_maturity_level(assessment.governance_score)
    tech_level, tech_name, _ = get_maturity_level(assessment.technical_debt_score)

    data = [
        ["Dimension", "Score", "Maturity Level"],
        ["Security", f"{assessment.security_score:.1f}", f"Level {sec_level}: {sec_name}"],
        ["Financial", f"{assessment.financial_score:.1f}", f"Level {fin_level}: {fin_name}"],
        ["Operational", f"{assessment.operational_score:.1f}", f"Level {op_level}: {op_name}"],
        ["Governance", f"{assessment.governance_score:.1f}", f"Level {gov_level}: {gov_name}"],
        ["Technical Debt", f"{assessment.technical_debt_score:.1f}", f"Level {tech_level}: {tech_name}"],
    ]
    t = Table(data, colWidths=[120, 100, 160])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ]
        )
    )
    el += [Paragraph("Dimension Scores", styles["Heading2"]), t, Spacer(1, 18)]

    el += [
        Paragraph("System Information", styles["Heading2"]),
        Paragraph(f"Name: {system.name}", styles["Normal"]),
        Paragraph(f"Description: {system.description}", styles["Normal"]),
        Paragraph(f"Created: {system.created_at:%Y-%m-%d}", styles["Normal"]),
    ]

    doc.build(el)
    return tmp.name

def generate_pdf_with_recommendations(assessment, system, financial_assessment=None):

    from app.recommendations import generate_recommendations_with_timeline

    recs, _, _ = generate_recommendations_with_timeline(
    assessment, financial_assessment
)

    # Get maturity level info
    level_num, level_name, _ = get_maturity_level(assessment.overall_score)

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    doc = SimpleDocTemplate(tmp.name, pagesize=letter)
    styles = getSampleStyleSheet()
    el = []

    # header
    el += [
        Paragraph("Legacy System Maturity Assessment Report", styles["Title"]),
        Paragraph(f"System: {system.name}", styles["Heading1"]),
        Paragraph(
            f"Date: {assessment.timestamp.strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"],
        ),
        Spacer(1, 18),
        Paragraph(
            f"Overall Maturity Score: {assessment.overall_score:.1f}/100 (Level {level_num}: {level_name})",
            styles["Heading2"],
        ),
        Spacer(1, 18),
    ]

    # Get maturity levels for each dimension
    sec_level, sec_name, _ = get_maturity_level(assessment.security_score)
    fin_level, fin_name, _ = get_maturity_level(assessment.financial_score)
    op_level, op_name, _ = get_maturity_level(assessment.operational_score)
    gov_level, gov_name, _ = get_maturity_level(assessment.governance_score)
    tech_level, tech_name, _ = get_maturity_level(assessment.technical_debt_score)

    # dimension table with maturity levels
    data = [
        ["Dimension", "Score", "Maturity Level"],
        ["Security", f"{assessment.security_score:.1f}", f"Level {sec_level}: {sec_name}"],
        ["Financial", f"{assessment.financial_score:.1f}", f"Level {fin_level}: {fin_name}"],
        ["Operational", f"{assessment.operational_score:.1f}", f"Level {op_level}: {op_name}"],
        ["Governance", f"{assessment.governance_score:.1f}", f"Level {gov_level}: {gov_name}"],
        ["Technical Debt", f"{assessment.technical_debt_score:.1f}", f"Level {tech_level}: {tech_name}"],
    ]
    t = Table(data, colWidths=[120, 100, 160])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ]
        )
    )
    el += [Paragraph("Dimension Scores", styles["Heading2"]), t, Spacer(1, 18)]

    # recommendations
    el.append(Paragraph("Recommendations", styles["Heading2"]))
    for priority in ("critical", "high", "medium", "low"):
        if recs[priority]:
            el.append(Paragraph(priority.capitalize(), styles["Heading4"]))
            for item in recs[priority]:
                el.append(Paragraph(f"• {item['text']}", styles["Normal"]))
            el.append(Spacer(1, 8))

    # optional financial summary
    if financial_assessment:
        fa = financial_assessment
        fin_score = fa.calculate_financial_score()
        fin_level, fin_name, _ = get_maturity_level(fin_score)
        
        el += [
            Spacer(1, 12),
            Paragraph("Financial Assessment Summary", styles["Heading2"]),
            Paragraph(
                f"Financial Maturity Level: Level {fin_level}: {fin_name}",
                styles["Normal"],
            ),
            Paragraph(
                f"Annual Security Budget: £{float(fa.annual_security_budget or 0):,.0f}",
                styles["Normal"],
            ),
            Paragraph(
                f"Planned Investment: £{float(fa.planned_security_investment or 0):,.0f}",
                styles["Normal"],
            ),
            Paragraph(
                f"Potential Breach Cost: £{float(fa.potential_breach_cost or 0):,.0f}",
                styles["Normal"],
            ),
            Paragraph(
                "Cyber Insurance: "
                + ("Yes" if fa.has_cyber_insurance == "yes" else "No"),
                styles["Normal"],
            ),
        ]
        if fa.has_cyber_insurance == "yes":
            el.append(
                Paragraph(
                    f"Insurance Coverage: £{float(fa.cyber_insurance_coverage or 0):,.0f}",
                    styles["Normal"],
                )
            )

    # system info
    el += [
        Spacer(1, 18),
        Paragraph("System Information", styles["Heading2"]),
        Paragraph(f"Name: {system.name}", styles["Normal"]),
        Paragraph(f"Description: {system.description}", styles["Normal"]),
        Paragraph(f"Created: {system.created_at:%Y-%m-%d}", styles["Normal"]),
    ]

    doc.build(el)
    return tmp.name


def generate_csv_export(assessment, system):
    tmp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    
    # Get maturity levels for each dimension
    level_num, level_name, _ = get_maturity_level(assessment.overall_score)
    sec_level, sec_name, _ = get_maturity_level(assessment.security_score)
    fin_level, fin_name, _ = get_maturity_level(assessment.financial_score)
    op_level, op_name, _ = get_maturity_level(assessment.operational_score)
    gov_level, gov_name, _ = get_maturity_level(assessment.governance_score)
    tech_level, tech_name, _ = get_maturity_level(assessment.technical_debt_score)
    
    with open(tmp.name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "System Name",
                "Assessment Date",
                "Overall",
                "Overall Level",
                "Security",
                "Security Level",
                "Financial",
                "Financial Level",
                "Operational",
                "Operational Level",
                "Governance",
                "Governance Level",
                "Technical Debt",
                "Technical Debt Level",
            ]
        )
        w.writerow(
            [
                system.name,
                assessment.timestamp.strftime("%Y-%m-%d %H:%M"),
                f"{assessment.overall_score:.1f}",
                f"Level {level_num}: {level_name}",
                f"{assessment.security_score:.1f}",
                f"Level {sec_level}: {sec_name}",
                f"{assessment.financial_score:.1f}",
                f"Level {fin_level}: {fin_name}",
                f"{assessment.operational_score:.1f}",
                f"Level {op_level}: {op_name}",
                f"{assessment.governance_score:.1f}",
                f"Level {gov_level}: {gov_name}",
                f"{assessment.technical_debt_score:.1f}",
                f"Level {tech_level}: {tech_name}",
            ]
        )
        w.writerow([])
        w.writerow(["Dimension", "Question", "Response (0-4)"])
        for r in assessment.responses:
            w.writerow(
                [r.dimension.capitalize(), get_question_text(r.question_id), r.response]
            )
    return tmp.name


#Financial-only PDF 
def generate_financial_pdf_report(financial_assessment):
    temp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    fa = financial_assessment
    
    # Get financial maturity level
    fin_score = fa.calculate_financial_score()
    fin_level, fin_name, _ = get_maturity_level(fin_score)
    
    elements.append(Paragraph("Financial Security Assessment", styles["Title"]))
    elements.append(Paragraph(f"Date: {fa.created_at.strftime('%Y-%m-%d')}", styles["Normal"]))
    elements.append(Paragraph(f"Maturity Level: Level {fin_level}: {fin_name}", styles["Normal"]))
    elements.append(Spacer(1, 16))

    
    data = [
        ["Metric", "Value (£)"],
        ["Annual security budget", f"{float(fa.annual_security_budget or 0):,.0f}"],
        ["Planned investment", f"{float(fa.planned_security_investment or 0):,.0f}"],
        ["Staff & training", f"{float(fa.security_staff_training or 0):,.0f}"],
        ["Annual revenue", f"{float(fa.annual_revenue or 0):,.0f}"],
        ["Potential fine", f"{float(fa.potential_fine or 0):,.0f}"],
        ["Potential breach cost", f"{float(fa.potential_breach_cost or 0):,.0f}"],
        ["Downtime / hr", f"{float(fa.downtime_cost_per_hour or 0):,.0f}"],
        ["Avg downtime hrs/yr", f"{fa.average_downtime_hours or 0:,}"],
        ["Cyber-insurance?", fa.has_cyber_insurance],
        ["Coverage", f"{float(fa.cyber_insurance_coverage or 0):,.0f}"],
        ["Calculated score", f"{fin_score:.1f}/100"],
        ["Maturity level", f"Level {fin_level}: {fin_name}"]
    ]
    t = Table(data, colWidths=[260, 140])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke)
    ]))
    elements.append(t)
    doc.build(elements)
    return temp_file.name


#Financial-only CSV
def generate_financial_csv_export(financial_assessment):
    temp_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)

    fa = financial_assessment
    fin_score = fa.calculate_financial_score()
    fin_level, fin_name, _ = get_maturity_level(fin_score)
    
    with open(temp_file.name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Field", "Value"])
        rows = [
            ("created_at", fa.created_at.isoformat()),
            ("annual_security_budget", fa.annual_security_budget),
            ("planned_security_investment", fa.planned_security_investment),
            ("security_staff_training", fa.security_staff_training),
            ("annual_revenue", fa.annual_revenue),
            ("potential_fine", fa.potential_fine),
            ("potential_breach_cost", fa.potential_breach_cost),
            ("downtime_cost_per_hour", fa.downtime_cost_per_hour),
            ("average_downtime_hours", fa.average_downtime_hours),
            ("acceptable_risk_level", fa.acceptable_risk_level),
            ("has_cyber_insurance", fa.has_cyber_insurance),
            ("cyber_insurance_coverage", fa.cyber_insurance_coverage),
            ("calculated_score", fin_score),
            ("maturity_level", f"Level {fin_level}: {fin_name}")
        ]
        w.writerows(rows)
    return temp_file.name


#Combined CSV 
def generate_combined_csv(assessment, system, financial_assessment, recommendations):
    temp_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)

    # Get maturity levels
    level_num, level_name, _ = get_maturity_level(assessment.overall_score)
    sec_level, sec_name, _ = get_maturity_level(assessment.security_score)
    fin_level, fin_name, _ = get_maturity_level(assessment.financial_score)
    op_level, op_name, _ = get_maturity_level(assessment.operational_score)
    gov_level, gov_name, _ = get_maturity_level(assessment.governance_score)
    tech_level, tech_name, _ = get_maturity_level(assessment.technical_debt_score)
    
    fa_score = financial_assessment.calculate_financial_score()
    fa_level, fa_name, _ = get_maturity_level(fa_score)

    with open(temp_file.name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        # System / assessment header
        w.writerow(["Section", "Field", "Value"])
        w.writerow(["System", "Name", system.name])
        w.writerow(["System", "ID", system.id])
        w.writerow(["Assessment", "ID", assessment.id])
        w.writerow(["Assessment", "Date", assessment.timestamp.isoformat()])
        w.writerow([])

        # Dimension scores with maturity levels
        w.writerow(["Dimension scores"])
        w.writerow(["Dimension", "Score", "Maturity Level"])
        dimension_scores = [
            ("Security", assessment.security_score, f"Level {sec_level}: {sec_name}"),
            ("Financial", assessment.financial_score, f"Level {fin_level}: {fin_name}"),
            ("Operational", assessment.operational_score, f"Level {op_level}: {op_name}"),
            ("Governance", assessment.governance_score, f"Level {gov_level}: {gov_name}"),
            ("Technical debt", assessment.technical_debt_score, f"Level {tech_level}: {tech_name}"),
            ("Overall", assessment.overall_score, f"Level {level_num}: {level_name}")
        ]
        w.writerows(dimension_scores)
        w.writerow([])

        #Financial assessment numbers
        fa = financial_assessment
        w.writerow(["Financial assessment"])
        for field in ["annual_security_budget","planned_security_investment",
                    "security_staff_training","annual_revenue","potential_fine",
                    "potential_breach_cost","downtime_cost_per_hour",
                    "average_downtime_hours","acceptable_risk_level",
                    "has_cyber_insurance","cyber_insurance_coverage"]:
            w.writerow([field, getattr(fa, field)])
        w.writerow(["calculated_score", fa_score])
        w.writerow(["maturity_level", f"Level {fa_level}: {fa_name}"])
        w.writerow([])

        #Recommendations
        w.writerow(["Recommendations"])
        w.writerow(["Priority", "Dimension", "Recommendation"])
        for priority, items in recommendations.items():
            for item in items:
                w.writerow([priority.upper(), item["dimension"], item["text"]])

    return temp_file.name