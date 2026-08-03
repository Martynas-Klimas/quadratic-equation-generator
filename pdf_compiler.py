import io
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.backends.backend_pdf import PdfPages


def compile_pdf(worksheet_data, title):
    pdf_buffer = io.BytesIO()

    with PdfPages(pdf_buffer) as pdf:

        # PAGE 1: STUDENT WORKSHEET

        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")

        fig.text(
            0.5,
            0.93,
            title.upper(),
            fontsize=20,
            weight="bold",
            ha="center",
            color="black",
        )
        fig.text(
            0.1,
            0.88,
            "STUDENT EXERCISES",
            fontsize=12,
            weight="bold",
            color="black",
        )

        current_y = 0.85

        for i, item in enumerate(worksheet_data):
            if current_y < 0.20:
                pdf.savefig(fig)
                plt.close(fig)

                fig, ax = plt.subplots(figsize=(8.5, 11))
                ax.axis("off")
                current_y = 0.85

            box_left = 0.1
            box_width = 0.8
            box_height = 0.18
            box_bottom = current_y - box_height

            rect = plt.Rectangle(
                (box_left, box_bottom),
                box_width,
                box_height,
                transform=fig.transFigure,
                facecolor="none",
                edgecolor="#333333",
                linewidth=1.2,
            )
            fig.patches.append(rect)

            badge_x = box_left + 0.025

            content_y = current_y - 0.025

            ASPECT_RATIO = 8.5 / 11.0

            badge = Ellipse(
                (badge_x, content_y),
                width=0.03,  
                height=0.03 * ASPECT_RATIO, 
                transform=fig.transFigure,
                facecolor="#000000",
            )
            fig.patches.append(badge)

            badge_text_y = content_y - 0.0015

            fig.text(
                badge_x,
                badge_text_y,
                str(i + 1),
                color="white",
                fontsize=10,
                weight="bold",
                ha="center",
                va="center",
            )

            fig.text(
                box_left + 0.05,
                content_y,
                f"${item['equation']}$",
                fontsize=13,
                weight="normal",
                va="center",
            )

            fig.text(
                box_left + box_width - 0.03,
                box_bottom + 0.025,
                "Answer:  ____________________",
                fontsize=10,
                weight="bold",
                ha="right",
                color="#000000",
            )

            current_y -= box_height + 0.025

        pdf.savefig(fig)
        plt.close(fig)

        # PAGE 2: TEACHER ANSWER KEY
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")

        fig.text(
            0.5,
            0.93,
            f"ANSWER KEY: {title.upper()}",
            fontsize=18,
            weight="bold",
            ha="center",
            color="black",
        )
        fig.text(
            0.1,
            0.88,
            "Tutor Reference Copy",
            fontsize=11,
            weight="bold",
            color="#444444",
        )

        current_y = 0.83

        for i, item in enumerate(worksheet_data):
            if current_y < 0.1:
                pdf.savefig(fig)
                plt.close(fig)
                fig, ax = plt.subplots(figsize=(8.5, 11))
                ax.axis("off")
                current_y = 0.85

            fig.text(
                0.1,
                current_y,
                f"Solution {i+1}:",
                fontsize=11,
                weight="bold",
                color="black",
            )

            latex_solution = f"${item['solution']}$"
            fig.text(
                0.15,
                current_y - 0.025,
                latex_solution,
                fontsize=12,
                color="black",
            )

            current_y -= 0.065

        pdf.savefig(fig)
        plt.close(fig)

    return pdf_buffer.getvalue()