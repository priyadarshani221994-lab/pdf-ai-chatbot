import streamlit as st
import requests

st.title("🤖 PDF AI Chatbot")

user_input = st.text_input("Ask Question")

if st.button("Send"):

    response = requests.get(
        f"http://127.0.0.1:8000/ask?query={user_input}"
    )

    data = response.json()

    st.write("Answer:")
    st.write(data["response"])