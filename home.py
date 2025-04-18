import streamlit as st
import pandas as pd

st.title("Stock performance") 
st.write("hello")

def generate_performance():
    msg = st.toast('Gathering ingredients...')
    msg.toast('Ready!', icon = "🥞")

if st.button('click'):
    generate_performance()
    st.balloons()