from fpdf import FPDF
from datetime import datetime


def generate():
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()

    pdf.set_font(family="Arial", style="B", size=14)
    pdf.cell(w=0, h=24, txt="Receipt for EM's Booking", align="L", ln=1)

    date = datetime.now().strftime("%d-%m-%Y")
    time = datetime.now().strftime("%I:%M:%S")

    pdf.set_font(family="Arial", style="", size=14)
    pdf.cell(w=0, h=25, txt=date, align="R")
    pdf.cell(w=0, h=35, txt=time,align="R", ln=1)

    pdf.output("receipt.pdf")


if __name__ == "__main__":
    generate()
    print("PDF has been generated")
