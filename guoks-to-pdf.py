import streamlit as st
import zipfile

uploaded_zip = st.file_uploader("Загрузите ZIP-файл", type=["zip"])
if uploaded_zip is not None:
    zf = zipfile.ZipFile(uploaded_zip)
    zf.extractall(".")
