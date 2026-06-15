from fpdf import FPDF


def clean_equation_text(raw_eq):
    # Translates computer-notation LaTeX into clean, human-readable textbook math symbols.

    clean = raw_eq.replace("\\quad", " ").strip()
    clean = clean.replace("= 0", " = 0")

    # Clean up standard variables and spacings
    clean = clean.replace("x^2", "x²")
    clean = clean.replace("-", "- ")

    return clean


def clean_solution_text(raw_sol):

    # Translates LaTeX logic strings into subscript notations for root answers.

    # Strip away backslashes and horizontal layout spacing variables
    clean = raw_sol.replace("\\quad", "   ").replace("\\", "").strip()

    # Map raw math characters to professional unicode subscript typography
    clean = clean.replace("x_1", "x₁")
    clean = clean.replace("x_2", "x₂")
    clean = clean.replace("frac{", "").replace(
        "}{", "/")  # Simulates small inline fractions
    clean = clean.replace("}", "")

    return clean


def compile_pdf(worksheet_data):
    pdf = FPDF(orientation="P", unit="mm", format="letter")
    pdf.set_auto_page_break(auto=True, margin=15)

    # PAGE 1: STUDENT COPY
    pdf.add_page()

    # Header Title
    pdf.set_font("Helvetica", style="B", size=22)
    pdf.cell(w=0, h=15, txt="Quadratic Equations Worksheet", ln=True, align="C")

    # Subtitle Accent
    pdf.set_font("Helvetica", style="B", size=13)
    pdf.set_text_color(43, 108, 176)  # Professional blue
    pdf.cell(w=0, h=8, txt="Student Exercises", ln=True, align="L")
    pdf.ln(5)

    # Print the questions
    pdf.set_text_color(45, 55, 72)
    for i, item in enumerate(worksheet_data):
        # Clean up LaTeX specific strings
        clean_eq = clean_equation_text(item["equation"])

        pdf.set_font("Helvetica", style="B", size=12)
        pdf.cell(w=0, h=6, txt=f"Exercise {i+1}:", ln=True)

        # Serif italic font for a standard math textbook look
        pdf.set_font("Times", style="I", size=14)
        pdf.cell(w=0, h=8, txt=f"      {clean_eq}", ln=True)
        pdf.ln(6)

    # PAGE 2: TUTOR COPY (Answer Key Only)

    pdf.add_page()

    pdf.set_font("Helvetica", style="B", size=22)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(w=0, h=15, txt="Master Answer Key", ln=True, align="C")

    pdf.set_font("Helvetica", style="B", size=13)
    pdf.set_text_color(43, 108, 176)
    pdf.cell(w=0, h=8, txt="Tutor Reference Copy", ln=True, align="L")
    pdf.ln(5)

    pdf.set_text_color(45, 55, 72)
    for i, item in enumerate(worksheet_data):
        clean_sol = clean_solution_text(item["solution"])

        pdf.set_font("Helvetica", style="B", size=12)
        pdf.write(h=6, txt=f"Solution {i+1}: ")

        pdf.set_font("Times", style="I", size=13)
        pdf.write(h=6, txt=f"{clean_sol}\n")
        pdf.ln(4)

    # Output as raw stream
    return bytes(pdf.output())
