# https://streamlit.io/generative-ai

import streamlit as st
from handler import generate_chat_completion

# Streamlit App
st.title("Health Chatbot Application") 

with st.form("my_input_form", clear_on_submit=True):   #https://docs.streamlit.io/develop/api-reference/execution-flow/st.form
    user_input = st.text_input("Type your prompt here")
    submit_button = st.form_submit_button(label="Submit prompt")

# Press button to generate response from chatbot

if submit_button:
    with st.spinner("A moment please...", show_time=True):   #https://docs.streamlit.io/develop/api-reference/status/st.spinner
        completion = generate_chat_completion(user_input)
        st.write(completion)