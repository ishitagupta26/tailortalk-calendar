import streamlit as st
from calendar_agent import run_calendar_agent
from dotenv import load_dotenv
import os
print("LOADED CLIENT EMAIL:", os.environ.get("client_email"))


# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="🧵 TailorTalk Calendar Assistant", layout="centered")

st.title("🧵 TailorTalk Calendar Assistant")
st.markdown("Chat with me to book appointments on your calendar!")

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input
query = st.chat_input("What can I help you with today?")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = run_calendar_agent(query)
            except Exception as e:
                response = f"❌ Sorry, something went wrong:\n\n```\n{str(e)}\n```"
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
