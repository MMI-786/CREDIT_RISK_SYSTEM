from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

# ---------------- SINGLE REPORT ----------------
def generate_report(result, prob):

    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Credit Risk Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Decision: {result}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Risk Probability: {round(prob,2)}", styles["Normal"]))

    doc.build(content)

# ---------------- FULL SYSTEM REPORT ----------------
def generate_full_report():

    doc = SimpleDocTemplate("full_report.pdf")
    styles = getSampleStyleSheet()

    content = []

    try:
        df = pd.read_csv("history.csv")

        content.append(Paragraph("System Report", styles["Title"]))
        content.append(Spacer(1, 12))

        content.append(Paragraph(f"Total Predictions: {len(df)}", styles["Normal"]))
        content.append(Paragraph(f"Average Risk: {round(df['probability'].mean(),2)}", styles["Normal"]))

    except:
        content.append(Paragraph("No data available", styles["Normal"]))

    doc.build(content)