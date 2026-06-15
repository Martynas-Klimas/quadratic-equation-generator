from fpdf import FPDF
import os


def compile_pdf(worksheet_data):
    pdf = FPDF(orientation="P", unit="mm", format="letter")
    pdf.set_auto_page_break(auto=True, margin=15)

    font_path = os.path.join("fonts", "STIXTwoMath-Regular.ttf")
    pdf.add_font("MathFont", style="", fname=font_path)

    # PAGE 1: STUDENT COPY
    pdf.add_page()

    # Header Title
    pdf.set_font("MathFont", size=22)
    pdf.cell(w=0, h=15, txt="Quadratic Equations Worksheet", ln=True, align="C")
    pdf.cell(w=0, h=8, txt="Student Exercises", ln=True, align="L")
    pdf.ln(5)

    # Print the questions
    for i, item in enumerate(worksheet_data):
        pdf.set_font("MathFont", size=12)
        pdf.cell(w=0, h=6, txt=f"Exercise {i+1}:", ln=True)

        clean_eq = item["equation"].replace("\\quad", "  ")

        # Serif italic font for a standard math textbook look
        pdf.set_font("MathFont", style="I", size=14)
        pdf.cell(w=0, h=8, txt=f"      {clean_eq}", ln=True)
        pdf.ln(6)

    # PAGE 2: TUTOR COPY (Answer Key Only)

    pdf.add_page()

    pdf.set_font("MathFont", size=22)
    pdf.cell(w=0, h=15, txt="Master Answer Key", ln=True, align="C")
    pdf.cell(w=0, h=8, txt="Tutor Reference Copy", ln=True, align="L")
    pdf.ln(5)

    for i, item in enumerate(worksheet_data):
        pdf.set_font("MathFont", size=12)
        pdf.write(h=6, txt=f"Solution {i+1}: ")

        clean_sol = item["solution"].replace("\\quad", "  ").replace("\\", "")

        pdf.set_font("MathFont", size=14)
        pdf.write(h=6, txt=f"{clean_sol}\n")
        pdf.ln(4)

    # Output as raw stream
    return bytes(pdf.output())
