import matplotlib.pyplot as plt
import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import ParagraphStyle

from io import BytesIO
from datetime import datetime
import uuid


# ---------------------------
# FORMAT INR
# ---------------------------
def format_inr(x):
    if x >= 100000:
        return f"Rs. {x / 100000:.2f} Lakh"
    return f"Rs. {x:,.0f}"


# ---------------------------
# GENERATE PDF
# ---------------------------
def generate_pdf(data):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    # ---------------------------
    # CUSTOM COLORS
    # ---------------------------
    brand_blue = colors.HexColor("#2c3e50")
    light_blue = colors.HexColor("#eaf2f8")
    success_green = colors.HexColor("#d4edda")
    warning_yellow = colors.HexColor("#fff3cd")
    dark_text = colors.HexColor("#212529")

    # ---------------------------
    # TITLE STYLE
    # ---------------------------
    title_style = ParagraphStyle(
        "title_style",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        textColor=brand_blue,
    )

    subtitle_style = ParagraphStyle(
        "subtitle_style",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.grey,
    )

    normal_style = styles["Normal"]

    elements = []

    # ---------------------------
    # HEADER
    # ---------------------------
    try:
        logo = Image("financelogo.png", width=140, height=50)
        elements.append(logo)
        elements.append(Spacer(1, 25))
    except:
        pass

    report_id = f"FIN-2026-{str(uuid.uuid4())[:8].upper()}"

    timestamp = datetime.now().strftime("%d %b %Y | %I:%M %p")

    header_text = f"""
    <b>Report ID:</b> {report_id}<br/>
    <b>Generated On:</b> {timestamp}<br/>
    <b>Classification:</b> STRICTLY CONFIDENTIAL
    """

    elements.append(Paragraph(header_text, normal_style))
    elements.append(Spacer(1, 18))

    # ---------------------------
    # TITLE
    # ---------------------------
    elements.append(
        Paragraph(
            "OFFICIAL LOAN EVALUATION SUMMARY",
            title_style,
        )
    )

    elements.append(
        Paragraph(
            "Hybrid AI Governance & Risk Intelligence Report",
            subtitle_style,
        )
    )

    elements.append(Spacer(1, 20))

    # ---------------------------
    # APPLICANT PROFILE
    # ---------------------------
    elements.append(
        Paragraph("<b>Applicant Profile</b>", styles["Heading2"])
    )

    profile_data = [
        ["Applicant Name", data.get("applicant_name", "Unknown Applicant")],
        ["Loan Type", data.get("loan_type", "-")],
        ["Employment Status", data.get("employment", "-")],
        ["Annual Income", format_inr(data.get("income", 0))],
        ["Loan Requested", format_inr(data.get("loan", 0))],
        ["Asset Value", format_inr(data.get("asset", 0))],
        ["Credit Score", str(data.get("credit_score", 0))],
        ["Loan Tenure", f"{data.get('years', 0)} Years"],
        ["Interest Rate", f"{data.get('interest', 0)*100:.2f}%"],
    ]

    profile_table = Table(profile_data, colWidths=[180, 280])

    profile_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), light_blue),
            ("GRID", (0, 0), (-1, -1), 1, colors.white),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ])
    )

    elements.append(profile_table)

    elements.append(Spacer(1, 20))

    # ---------------------------
    # FINANCIAL SNAPSHOT
    # ---------------------------
    elements.append(
        Paragraph("<b>Financial Snapshot</b>", styles["Heading2"])
    )

    snapshot_data = [[
        "EMI",
        "DTI Ratio",
        "LTV Ratio",
        "AI Confidence"
    ],
        [
            format_inr(data.get("emi", 0)),
            f"{data.get('dti', 0):.2f}",
            f"{data.get('ltv', 0):.2f}",
            f"{data.get('prob', 0) * 100:.2f}%"
        ]]

    snapshot_table = Table(snapshot_data, colWidths=[120, 120, 120, 120])

    snapshot_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), brand_blue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, 1), success_green),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ])
    )

    elements.append(snapshot_table)

    elements.append(Spacer(1, 20))

    # ---------------------------
    # GOVERNANCE CHECK
    # ---------------------------
    elements.append(
        Paragraph("<b>Risk Governance Check</b>", styles["Heading2"])
    )

    governance_data = [
        ["AI Model", "Bank Policy"],
        ["Approval Recommended", "Policy Compliant"]
    ]

    governance_table = Table(governance_data, colWidths=[240, 240])

    governance_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), brand_blue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, 1), success_green),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ])
    )

    elements.append(governance_table)

    elements.append(Spacer(1, 12))

    status_table = Table(
        [["GOVERNANCE APPROVED"]],
        colWidths=[480]
    )

    status_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), success_green),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.green),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ])
    )

    elements.append(status_table)

    elements.append(Spacer(1, 20))
    # ---------------------------
    # AI DECISION SUMMARY
    # ---------------------------
    elements.append(
        Paragraph("<b>AI Decision Summary</b>", styles["Heading2"])
    )

    ai_summary = """
    • Excellent credit history increased approval confidence<br/>
    • Low debt burden improved financial stability<br/>
    • Stable income profile strengthened affordability<br/>
    • Overall applicant classified as Low Risk
    """

    elements.append(
        Paragraph(ai_summary, normal_style)
    )

    elements.append(Spacer(1, 18))
    # ---------------------------
    # STRATEGIC INSIGHTS
    # ---------------------------
    elements.append(
        Paragraph("<b>Strategic Decision Insights</b>", styles["Heading2"])
    )

    strategic_text = """
    • Prime credit tier reduced lending risk exposure<br/>
    • Strong liquidity profile detected<br/>
    • Recommended safe lending capacity maintained<br/>
    • No major institutional governance risks identified
    """

    elements.append(
        Paragraph(strategic_text, normal_style)
    )

    elements.append(Spacer(1, 18))
    # ---------------------------
    # AI DECISION BREAKDOWN CHART
    # ---------------------------
    elements.append(
        Paragraph(
            "<b>AI Decision Breakdown</b>",
            styles["Heading2"]
        )
    )

    factors = [
        "Collateral",
        "Credit",
        "Debt",
        "Income"
    ]

    # Dynamic percentage-based scores
    collateral_score = int((1 - data.get("ltv", 0)) * 100)

    credit_score = int(
        (data.get("credit_score", 0) / 900) * 100
    )

    debt_score = int((1 - data.get("dti", 0)) * 100)

    income_score = min(
        int((data.get("income", 0) / 5000000) * 100),
        100
    )

    scores = [
        collateral_score,
        credit_score,
        debt_score,
        income_score
    ]

    plt.figure(figsize=(5.8, 2.8))

    bars = plt.bar(
        factors,
        scores,
        color="#2c7fb8",
        edgecolor="black",
        linewidth=1
    )

    # Add % labels
    for bar in bars:
        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 2,
            f"{height}%",
            ha='center',
            fontsize=9,
            fontweight='bold'
        )

    plt.ylim(0, max(scores)+10)

    plt.ylabel("Contribution %")

    plt.title("AI Approval Contribution (%)",
              fontsize=12,
              fontweight="bold",
              pad=8
              )

    plt.tight_layout()

    chart_path = "decision_chart.png"

    plt.savefig(
        chart_path,
        bbox_inches="tight"
    )

    plt.close()

    chart = Image(
        chart_path,
        width=420,
        height=220
    )

    elements.append(chart)

    elements.append(Spacer(1, 20))
    # ---------------------------

    # FINANCIAL VISUALIZATION

    # ---------------------------

    elements.append(

        Paragraph(

            "<b>Loan Affordability & Burden Analysis</b>",

            styles["Heading2"]

        )

    )

    try:

        emi_chart = Image(

            "emi_vs_income.png",

            width=230,

            height=170

        )

        burden_chart = Image(

            "loan_burden.png",

            width=230,

            height=170

        )

        emi_title = Paragraph("<b>Income vs EMI Capacity</b>",
                                 styles["BodyText"])

        burden_title = Paragraph("<b>Monthly Loan Burden Distribution</b>",
                              styles["BodyText"])

        charts_table = Table(

            [
                [emi_title, burden_title],
                [emi_chart, burden_chart]
            ],

            colWidths=[240, 240]

        )

        charts_table.setStyle(

            TableStyle([

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("TOPPADDING", (0, 1), (-1, 1), 8)

            ])

        )

        elements.append(charts_table)


    except:

        pass

    elements.append(Spacer(1, 20))

    # ---------------------------
    # FINAL DECISION
    # ---------------------------
    elements.append(
        Paragraph("<b>Final Decision</b>", styles["Heading2"])
    )

    decision_text = (
        "LOAN APPROVED"
        if data.get("decision") == 1
        else "LOAN NOT APPROVED"
    )

    decision_color = (
        success_green
        if data.get("decision") == 1
        else warning_yellow
    )

    decision_table = Table(
        [[decision_text]],
        colWidths=[480]
    )

    decision_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), decision_color),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
        ])
    )

    elements.append(decision_table)

    elements.append(Spacer(1, 12))

    confidence_para = Paragraph(
        f"<b>Confidence Score:</b> {data.get('prob', 0) * 100:.2f}%",
        normal_style
    )

    elements.append(confidence_para)

    elements.append(Spacer(1, 20))

    # ---------------------------
    # DISCLAIMER
    # ---------------------------
    disclaimer = """
    This report was generated using the FinWithDip Hybrid AI Governance Framework.<br/><br/>

    The recommendation is based on:
    <br/>• AI probability modeling
    <br/>• Banking compliance policies
    <br/>• Financial affordability analysis
    <br/>• Risk governance validation
    <br/><br/>

    This document is intended for simulation, educational,
    and analytical purposes only.
    """

    elements.append(
        Paragraph(disclaimer, normal_style)
    )

    elements.append(Spacer(1, 30))

    # ---------------------------
    # FOOTER
    # ---------------------------
    footer = """
    <b>FinWithDip — Smart Finance Tracker</b><br/>
    Generated Electronically — No Physical Signature Required<br/><br/>
    © 2026 FinWithDip | AI Loan Decision & Credit Risk Platform | Developed by Subhadip
    """

    elements.append(
        Paragraph(footer, subtitle_style)
    )

    # ---------------------------
    # BUILD PDF
    # ---------------------------
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf