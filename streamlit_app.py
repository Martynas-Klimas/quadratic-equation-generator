import streamlit as st
import random
from fractions import Fraction

a_special_cases = {1: "x^2", -1: "-x^2"}
b_special_cases = { 1:"+ x", -1: "- x", 0: ""}
c_special_cases = {0:""}

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

st.title("Quadratic equation generator")
st.write("Let's start generating!")

# Hidden print layout CSS styles injected right into the webpage header
st.markdown("""
    <style>
        @media print {
            /* Hide user controls, sidebars, buttons, and decorative breaks */
            header, [data-testid="stSidebar"], .stButton, iframe, hr {
                display: none !important;
            }
            
            /* Flatten application container backgrounds for standard white paper margins */
            .main .block-container {
                padding-top: 15mm !important;
                padding-bottom: 15mm !important;
                max-width: 100% !important;
            }
            
            /* Force closed expander boxes to snap wide open automatically on paper */
            [data-testid="stExpander"] div {
                display: block !important;
                height: auto !important;
                opacity: 1 !important;
            }
            
            /* Custom CSS class to drop a structural page break when printing */
            .print-page-break {
                page-break-before: always;
                display: block;
            }
        }
    </style>
""", unsafe_allow_html=True)

# 1. Initialize State Storage Memory
if "current_worksheet" not in st.session_state:
    st.session_state.current_worksheet = []

exercise_amount = st.slider("Choose number of exercises", 1, 10, 5, 1, )
option = st.radio("Choose exercise type", ["Simple quadratic equation", "Advanced quadratic equation", "Both (Mixed)"])

if st.button("🔄 Generate Exercises") or not st.session_state.current_worksheet:
    if option == "Simple quadratic equation":
        st.session_state.current_worksheet = generate_simple_equation(exercise_amount)
        
    elif option == "Advanced quadratic equation":
        st.session_state.current_worksheet = generate_advanced_equation(exercise_amount)
        
    else:  # "Both (Mixed)" option
        half = exercise_amount // 2
        remainder = exercise_amount - half
        
        # Call both functions separately and combine their outputs together!
        simple_part = generate_simple_equation(half)
        advanced_part = generate_advanced_equation(remainder)
        
        combined_list = simple_part + advanced_part
        # Shuffle the mixed items so they are randomly distributed
        random.shuffle(combined_list)
        
        st.session_state.current_worksheet = combined_list

# Frontend
if st.session_state.current_worksheet:
    st.write("---")
    st.write("### 📝 Current Worksheet Preview")
    
    # The Student's Question Sheet
    st.markdown("#### Exercises")
    for idx, item in enumerate(st.session_state.current_worksheet):
        st.write(f"**Exercise {idx+1}:**")
        st.write(f"$${item['equation']}$$")
        st.write("")  # Adds small spacing buffers between rows
        
    # Break Element: Active only when printed to separate pages!
    st.markdown('<div class="print-page-break"></div>', unsafe_allow_html=True)
    
    # Solution Key Sheet
    st.write("---")
    st.markdown("#### Answer Key Solutions")
    for idx, item in enumerate(st.session_state.current_worksheet):
        with st.expander(f"Solution Key for Exercise {idx+1}"):
            st.write(f"$${item['solution']}$$")
            
    # Print Dialog Action Trigger
    st.write("---")
    st.write("### Export Options:")
    st.components.v1.html(
        """
        <button style="
            background-color: #FF4B4B; color: white; border: none; 
            padding: 12px 24px; font-size: 16px; border-radius: 8px; 
            cursor: pointer; width: 100%; font-family: sans-serif;
            font-weight: bold;
        " onclick="window.parent.print()">Format & Save Worksheet as PDF</button>
        """,
        height=60,
    )