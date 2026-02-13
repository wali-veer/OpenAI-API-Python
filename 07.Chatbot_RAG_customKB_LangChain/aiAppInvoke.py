# https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps

import streamlit as st
import openai
import os
from dotenv import load_dotenv
from mainProgram import query

# Load the environment variables from .env file
load_dotenv()

# Assign the environmnet variables and select the LLM model
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY
#MODEL_ENGINE = "gpt-4o-mini"

st.title("Company Support Chatbot!")
chat_placeholder = st.empty()  #https://docs.streamlit.io/develop/api-reference/layout/st.empty

# https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
# Chat session history
def start_chat_history():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful agent acting as customer support agent."}
        ]


def start_chat():
    # Show the all the chat messages from history when application is rerun 
    # https://docs.streamlit.io/develop/api-reference/layout/st.empty
    with chat_placeholder.container():
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    # Allow users to enter their queries
    prompt = st.chat_input("Please enter your query?")
    if prompt :    
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):  #https://docs.streamlit.io/develop/api-reference/chat/st.chat_message
            st.markdown(prompt)

        # Generate response from Chat models
        response = query(prompt)

        # message_placeholder.markdown(response)
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    start_chat_history()
    start_chat()