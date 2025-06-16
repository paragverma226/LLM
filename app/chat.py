import streamlit as st
from chains.rag_chain import get_rag_chain

def run_chat():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("What would you like to do?")
    if user_input:
        with st.spinner("Thinking..."):
            qa_chain = get_rag_chain()
            response = qa_chain.run(user_input)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", response))

    for sender, msg in st.session_state.chat_history:
        st.chat_message("user" if sender == "You" else "assistant").write(msg)
