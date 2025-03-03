# src/frontend/main.py
import streamlit as st
import requests
import json

# App configuration
st.set_page_config(
    page_title="Scientific Paper Research Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# UI Header
st.title("Scientific Paper Research Assistant")
st.markdown("Ask questions about scientific papers, and I'll help you find and analyze relevant research.")

# User input
with st.form(key="question_form"):
    user_question = st.text_area("Enter your research question:", height=100)
    submit_button = st.form_submit_button("Submit")

# Process the question when submitted
if submit_button and user_question:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    # Show loading indicator
    with st.spinner("Researching your question..."):
        # Send request to backend
        response = requests.post(
            "http://localhost:8000/api/query",
            json={"query": user_question}
        )
        
        if response.status_code == 200:
            answer = response.json().get("answer", "Sorry, I couldn't process your request.")
            # Add assistant response to chat
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"Error: {response.status_code}")
            st.session_state.messages.append({"role": "assistant", "content": "Sorry, there was an error processing your request."})

# Display chat history
st.subheader("Conversation History")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Assistant:** {message['content']}")
    st.divider()