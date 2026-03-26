from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

def generate_report(result, prob):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Credit Risk Report", styles["Title"]))
    content.append(Paragraph(f"Risk: {result}", styles["Normal"]))
    content.append(Paragraph(f"Probability: {prob}", styles["Normal"]))

    doc.build(content)

def generate_full_report():
    doc = SimpleDocTemplate("full_report.pdf")
    styles = getSampleStyleSheet()

    content = []

    try:
        df = pd.read_csv("history.csv")

        content.append(Paragraph("System Report", styles["Title"]))
        content.append(Paragraph(f"Total Predictions: {len(df)}", styles["Normal"]))
        content.append(Paragraph(f"Average Risk: {round(df['probability'].mean(),2)}", styles["Normal"]))

    except:
        content.append(Paragraph("No data available", styles["Normal"]))

    doc.build(content)