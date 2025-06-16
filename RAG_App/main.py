import streamlit as st
from app.chat import run_chat

st.set_page_config(page_title="RAG Chatbot", layout="centered")
st.title("🎯 RAG Activity Recommendation Chatbot")

run_chat()