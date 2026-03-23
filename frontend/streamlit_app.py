import streamlit as st
import requests

st.title("SQL RAG Assistant")

q = st.text_input("Ask Question")

if st.button("Ask"):

    res = requests.get(
        "http://127.0.0.1:8000/ask",
        params={"question":q}
    )

    data = res.json()

    st.subheader("Generated SQL")
    st.code(data["sql"])

    st.subheader("Result")
    st.text(data["result"])