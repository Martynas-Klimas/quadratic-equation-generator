import streamlit as st
import random


b_special_cases = {
        1:"+ x",
        -1: "- x",
        0: ""
}

c_special_cases = {
        0:"",
}

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

        st.latex(f"{a_string} {b_string} {c_string} = 0")

        with st.expander("Show Solution Key"):
                st.write(f"Answers: $x = {r1}, x = {r2}$")

st.title("Quadratic equation generator")
st.write(
    "Let's start generating!"
)

st.write("Your quadratic equations is: ")

exercise_amount = st.slider("Choose number of exercises", 1, 10, 5, 1, )

generate_simple_equation(exercise_amount)

