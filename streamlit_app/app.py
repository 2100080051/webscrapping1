import streamlit as st
import requests

st.set_page_config(page_title="Smart Web QA", page_icon="🔍")
st.title("🔍 Ask Anything – Web-Powered AI Chatbot")
st.write("Type your question and get an AI-powered answer based on real-time web results.")

query = st.text_input("Ask a question:", placeholder="e.g. What is the latest update on AI research?")

if st.button("Get Answer") and query:
    with st.spinner("Searching the web and generating an answer..."):
        try:
            response = requests.post("https://flask-backend-by8v.onrender.com/ask", json={"query": query})
            if response.status_code == 200:
                answer = response.json().get("answer")
                st.success("Here's what I found:")
                st.markdown(answer)
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
