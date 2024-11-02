import requests
import streamlit as st

st.title("Meu Primeiro Chat GEPETO")

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
if prompt := st.chat_input("What's is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Estou pensando"):
            req = requests.post("http://localhost:8000/chat/chat/", 
                                json={"message": prompt} )
            response = req.json()
            st.markdown(response["assistant"])
    st.session_state.messages.append({"role": "assistant",
                                      "content": response["assistant"]})