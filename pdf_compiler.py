import io
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.backends.backend_pdf import PdfPages


def compile_pdf(worksheet_data, title):
    pdf_buffer = io.BytesIO()

    with PdfPages(pdf_buffer) as pdf:

        # HELPER FUNCTION FOR HEADERS 
        def draw_main_header(fig, title_text):
            fig.text(
                0.5,
                0.93,
                title_text.upper(),
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

        def draw_running_header(fig, title_text, page_num):
            fig.text(
                0.1,
                0.94,
                f"{title_text.upper()} — Page {page_num}",
                fontsize=12,
                color="#666666",
                style="italic",
            )


        # PAGE 1: STUDENT WORKSHEET

        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")

        draw_main_header(fig, title)

        current_y = 0.85
        page_num = 1

        for i, item in enumerate(worksheet_data):
            if current_y < 0.20:
                pdf.savefig(fig)
                plt.close(fig)

                fig, ax = plt.subplots(figsize=(8.5, 11))
                ax.axis("off")

                page_num += 1
                draw_running_header(fig, title, page_num)

                current_y = 0.90

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

        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")

        #PAGE 2: Teacher answer key

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

        col = 0  
        col_x_offsets = [0.1, 0.55] 
        top_y = 0.83
        current_y = top_y

        for i, item in enumerate(worksheet_data):
            if current_y < 0.1:
                if col == 0:
                    col = 1
                    current_y = top_y
                else:
                    pdf.savefig(fig)
                    plt.close(fig)

                    fig, ax = plt.subplots(figsize=(8.5, 11))
                    ax.axis("off")

                    col = 0
                    current_y = top_y

            x_label = col_x_offsets[col]
            x_solution = x_label + 0.05

            fig.text(
                x_label,
                current_y,
                f"Solution {i+1}:",
                fontsize=11,
                weight="bold",
                color="black",
            )

            latex_solution = f"${item['solution']}$"
            fig.text(
                x_solution,
                current_y - 0.025,
                latex_solution,
                fontsize=12,
                color="black",
            )

            current_y -= 0.065

        pdf.savefig(fig)
        plt.close(fig)

    return pdf_buffer.getvalue()