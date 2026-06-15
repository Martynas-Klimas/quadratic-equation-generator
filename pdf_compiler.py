# Inside pdf_compiler.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io


def compile_pdf(worksheet_data):
    pdf_buffer = io.BytesIO()

    with PdfPages(pdf_buffer) as pdf:

        # PAGE 1: STUDENT WORKSHEET (With Math Gridlines)
        fig, ax = plt.subplots(figsize=(8.5, 11))

        ax.axis('off')

        fig.text(0.5, 0.94, "Quadratic Equations Worksheet", fontsize=22, weight='bold',
                 ha='center', bbox=dict(facecolor='white', edgecolor='none', pad=4))
        fig.text(0.1, 0.89, "Student Exercises", fontsize=13, weight='bold',
                 color='#2b6cb0', bbox=dict(facecolor='white', edgecolor='none', pad=2))

        current_y = 0.86

        for i, item in enumerate(worksheet_data):
            if current_y < 0.19:
                pdf.savefig(fig)
                plt.close(fig)

                fig, ax = plt.subplots(figsize=(8.5, 11))
                ax.axis('off')
                current_y = 0.85

            box_left = 0.1
            box_width = 0.8
            box_height = 0.20
            box_bottom = current_y - box_height

            rect = plt.Rectangle(
                (box_left, box_bottom), box_width, box_height,
                transform=fig.transFigure,
                facecolor='none', edgecolor='#cbd5e1', linewidth=1.5
            )
            fig.patches.append(rect)

            combined_text = f"Exercise {i+1}:   ${item['equation']}$"

            fig.text(
                box_left + 0.02,
                current_y - 0.03,
                combined_text,
                fontsize=13,
                weight='normal'
            )

            current_y -= (box_height + 0.03)

        pdf.savefig(fig)
        plt.close(fig)

        # PAGE 2: TEACHER ANSWER KEY

        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')

        fig.text(0.5, 0.92, "Answer Key",
                 fontsize=22, weight='bold', ha='center')
        fig.text(0.1, 0.86, "Tutor Reference Copy Only",
                 fontsize=13, weight='bold', color='#2b6cb0')

        current_y = 0.82

        for i, item in enumerate(worksheet_data):
            if current_y < 0.1:
                pdf.savefig(fig)
                plt.close(fig)
                fig, ax = plt.subplots(figsize=(8.5, 11))
                ax.axis('off')
                current_y = 0.85

            fig.text(0.1, current_y,
                     f"Solution {i+1}:", fontsize=12, weight='bold')

            latex_solution = f"${item['solution']}$"
            fig.text(0.15, current_y - 0.03, latex_solution, fontsize=13)

            current_y -= 0.07

        pdf.savefig(fig)
        plt.close(fig)

    return pdf_buffer.getvalue()
