import streamlit as st
import random
from fractions import Fraction
from pdf_compiler import compile_pdf

st.markdown("""
    <style>
        /* Vaporize the header hover link chains */
        .e16fv1kl0 a {
            display: none !important;
        }
        h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)


a_special_cases = {1: "x^2", -1: "-x^2"}
b_special_cases = {1: "+ x", -1: "- x", 0: ""}
c_special_cases = {0: ""}


def format_latex_fraction(numerator, denominator):
    f = Fraction(numerator, denominator)

    num = f.numerator
    den = f.denominator

    if den == 1:
        return f"{num}"

    if num < 0:
        return f"-\\frac{{{abs(num)}}}{{{den}}}"

    return f"\\frac{{{num}}}{{{den}}}"


def generate_simple_equation(exercise_amount):
    problems = []
    for _ in range(exercise_amount):
        r1 = random.randint(-10, 10)
        r2 = random.randint(-10, 10)

        while r1 == 0 and r2 == 0:
            r2 = random.randint(-10, 10)

        b = -(r1 + r2)
        c = r1 * r2

        b_sign = "+" if b > 0 else ""
        c_sign = "+" if c > 0 else ""

        a_string = "x^2"
        b_string = b_special_cases.get(b, f"{b_sign} {b}x")
        c_string = c_special_cases.get(c, f"{c_sign} {c}")

        eq_latex = f"{a_string} {b_string} {c_string} = 0"

        if r1 != r2:
            sol_latex = f"x_1 = {r1}, \\quad x_2 = {r2}"
        else:
            sol_latex = f"x_1 = x_2 = {r1}"

        problems.append({"equation": eq_latex, "solution": sol_latex})

    return problems


def generate_advanced_equation(exercise_amount):
    problems = []
    for _ in range(exercise_amount):
        d1 = random.choice([-3, -2, -1, 2, 3])
        d2 = random.choice([2, 3])

        r1 = random.randint(-10, 10)
        r2 = random.randint(-10, 10)

        while r1 == 0 and r2 == 0:
            r2 = random.randint(-10, 10)

        a = d1 * d2
        b = -(d1 * r2 + d2 * r1)
        c = r1 * r2

        b_sign = "+" if b > 0 else ""
        c_sign = "+" if c > 0 else ""

        a_string = a_special_cases.get(a, f"{a}x^2")
        b_string = b_special_cases.get(b, f"{b_sign} {b}x")
        c_string = c_special_cases.get(c, f"{c_sign} {c}")

        eq_latex = f"{a_string} {b_string} {c_string} = 0"

        root1_latex = format_latex_fraction(r1, d1)
        root2_latex = format_latex_fraction(r2, d2)

        if root1_latex != root2_latex:
            sol_latex = f"x_1 = {root1_latex}, \\quad x_2 = {root2_latex}"
        else:
            sol_latex = f"x_1 = x_2 = {root1_latex}"

        problems.append({"equation": eq_latex, "solution": sol_latex})

    return problems


# Initialize State Storage Memory
if "current_worksheet" not in st.session_state:
    st.session_state.current_worksheet = []

st.title("Quadratic equation generator")
st.write("Let's start generating!")

with st.container():
    col1, col2 = st.columns([2, 1], vertical_alignment="center", gap="small")
    with col1:
        st.subheader("Generation Options")
        exercise_amount = st.slider("Choose number of exercises:", 1, 10, 5, 1, )

        option = st.radio("Choose exercise type:", [
                "Simple quadratic equation", "Advanced quadratic equation", "Both (Mixed)"])

        custom_title = st.text_input(
            label="Worksheet Title:", 
            value="Quadratic Equation Worksheet",
            help="This text will print as the main heading at the top of your PDF."
        )

        if st.button("🔄 Generate Exercises") or not st.session_state.current_worksheet:
            if option == "Simple quadratic equation":
                st.session_state.current_worksheet = generate_simple_equation(
                    exercise_amount)

            elif option == "Advanced quadratic equation":
                st.session_state.current_worksheet = generate_advanced_equation(
                    exercise_amount)

            else:  
                half = exercise_amount // 2
                remainder = exercise_amount - half

                simple_part = generate_simple_equation(half)
                advanced_part = generate_advanced_equation(remainder)

                combined_list = simple_part + advanced_part
                random.shuffle(combined_list)

                st.session_state.current_worksheet = combined_list
    with col2:
        st.subheader("Export Options")
        if "current_worksheet" in st.session_state and st.session_state.current_worksheet:
            if custom_title == "":
                custom_title = "Quadratic equation worksheet"
            pdf_bytes = compile_pdf(st.session_state.current_worksheet, custom_title)
            st.download_button(
                label="Download Printable PDF (Worksheet + Answer Key)",
                data=pdf_bytes,
                file_name=f"{custom_title.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.info("Click 'Generate' to create your download package.")

# CLEAN LAYOUT RENDERING STEP
st.write("---")
st.write("### Your Generated Exercises:")

for i, item in enumerate(st.session_state.current_worksheet):
    # Split the row into two clean columns
    col1, col2 = st.columns(2, vertical_alignment="center")

    with col1:
        st.write(f"**Exercise {i+1}:**")
        st.write(f"$${item['equation']}$$")

    with col2:
        # Sneak a blank string in to visually balance vertical alignment with the equation
        st.write("")
        with st.expander("Show Solution"):
            st.write(f"$${item['solution']}$$")

st.write("---")