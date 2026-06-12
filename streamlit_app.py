import streamlit as st
import random
from fractions import Fraction

a_special_cases = {
     1: "x^2",
     -1: "-x^2"
}

b_special_cases = {
        1:"+ x",
        -1: "- x",
        0: ""
}

c_special_cases = {
        0:"",
}

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
    for i in range(exercise_amount):
        r1 = random.randint(-10, 10)
        r2 = random.randint(-10, 10)

        b = -(r1 + r2)
        c = r1 * r2

        while r1 == 0 and r2 == 0:
            r2 = random.randint(-10, 10)

        b_sign = "+" if b > 0 else ""
        c_sign = "+" if c > 0 else ""

        a_string = "x^2"
        b_string = b_special_cases.get(b, f"{b_sign} {b}x")
        c_string = c_special_cases.get(c, f"{c_sign} {c}")
        
        st.write(f"Exercise {i+1}:")
        st.latex(f"{a_string} {b_string} {c_string} = 0")

        with st.expander("Show Solution Key"):
                st.write(f"Answers: $x = {r1}, x = {r2}$")

def generate_advanced_equation(exercise_amount):
    for i in range(exercise_amount):
        d1 = random.choice([-3, -2, -1, 2, 3])
        d2 = random.choice([2, 3])

        r1 = random.randint(-10, 10)
        r2 = random.randint(-10, 10)

        a = d1 * d2
        b = -(d1 * r2 + d2 * r1)
        c = r1 * r2

        while r1 == 0 and r2 == 0:
            r2 = random.randint(-10, 10)

        b_sign = "+" if b > 0 else ""
        c_sign = "+" if c > 0 else ""

        a_string = a_special_cases.get(a, f"{a}x^2")
        b_string = b_special_cases.get(b, f"{b_sign} {b}x")
        c_string = c_special_cases.get(c, f"{c_sign} {c}")
        
        st.write(f"Exercise {i+1}:")
        st.latex(f"{a_string} {b_string} {c_string} = 0")

        root1_latex = format_latex_fraction(r1, d1)
        root2_latex = format_latex_fraction(r2, d2)

        with st.expander("Show Solution Key"):
                st.write(f"Answers: $x_1 = {root1_latex}, x_2 = {root2_latex}$")



st.title("Quadratic equation generator")
st.write(
    "Let's start generating!"
)

st.write("Your quadratic equations is: ")

exercise_amount = st.slider("Choose number of exercises", 1, 10, 5, 1, )

generate_simple_equation(exercise_amount)

generate_advanced_equation(exercise_amount)

