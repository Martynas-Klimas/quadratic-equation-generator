# Inside pdf_compiler.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io


def compile_pdf(worksheet_data):
    pdf_buffer = io.BytesIO()

    with PdfPages(pdf_buffer) as pdf:

        # PAGE 1: STUDENT WORKSHEET (Questions Only)

        # Set up a standard Letter-sized layout (8.5 x 11 inches)
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')

        fig.text(0.5, 0.92, "Quadratic Equations Worksheet",
                 fontsize=22, weight='bold', ha='center')
        fig.text(0.1, 0.86, "Student Exercises Copy",
                 fontsize=13, weight='bold', color='#2b6cb0')

        current_y = 0.78

        for i, item in enumerate(worksheet_data):
            # Check if we are running out of room on the page; if so, create a new page
            if current_y < 0.1:
                pdf.savefig(fig)
                plt.close(fig)
                fig, ax = plt.subplots(figsize=(8.5, 11))
                ax.axis('off')
                current_y = 0.85

            fig.text(0.1, current_y,
                     f"Exercise {i+1}:", fontsize=11, weight='bold')

            latex_equation = f"${item['equation']}$"
            fig.text(0.15, current_y - 0.04, latex_equation, fontsize=15)

            current_y -= 0.12

        pdf.savefig(fig)
        plt.close(fig)

        # PAGE 2: TEACHER ANSWER KEY (Solutions Only)

        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')

        fig.text(0.5, 0.92, "Master Answer Key",
                 fontsize=22, weight='bold', ha='center')
        fig.text(0.1, 0.86, "Tutor Reference Copy Only",
                 fontsize=13, weight='bold', color='#2b6cb0')

        current_y = 0.78

        for i, item in enumerate(worksheet_data):
            if current_y < 0.1:
                pdf.savefig(fig)
                plt.close(fig)
                fig, ax = plt.subplots(figsize=(8.5, 11))
                ax.axis('off')
                current_y = 0.85

            fig.text(0.1, current_y,
                     f"Solution {i+1}:", fontsize=11, weight='bold')

            latex_solution = f"${item['solution']}$"
            fig.text(0.15, current_y - 0.04, latex_solution, fontsize=14)

            current_y -= 0.12

        pdf.savefig(fig)
        plt.close(fig)

    return pdf_buffer.getvalue()
