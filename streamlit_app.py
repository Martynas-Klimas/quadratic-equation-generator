import streamlit as st
import random


st.title("Quadratic equation generator")
st.write(
    "Let's start generating!"
)

a = random.choice(list(set(range(-5, 5)) - set([0])))
b = random.choice(list(set(range(-5, 5)) - set([0])))
c = random.randint(-20, 20)

st.write("Your quadratic equations is: ")
b_sign = "+" if b > 0 else ""
c_sign = "+" if c > 0 else ""

st.latex(f"{a}x^2 {b_sign} {b}x {c_sign}{c}")