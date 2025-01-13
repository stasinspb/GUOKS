import streamlit as st

uploaded_file = st.file_uploader("Загрузите ZIP-файл", type=["zip"])

if uploaded_file is not None:
    st.title(os.path.dirname(uploaded_file))
