import streamlit as st

uploaded_zip = st.file_uploader('XML File', type="zip", encoding="latin1")
    if uploaded_zip is not None:
        zf = zipfile.ZipFile(uploaded_zip)
        zf.extractall(".")
