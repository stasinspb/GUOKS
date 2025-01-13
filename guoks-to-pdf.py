import streamlit as st
import zipfile
import os

uploaded_zip = st.file_uploader("Загрузите ZIP-файл", type=["zip"])
if uploaded_zip is not None:
    zf = zipfile.ZipFile(uploaded_zip)
    zf.extractall(".")
    zf.close()
st.success("Распаковано")
st.success(os.getcwd())
st.success(os.listdir(os.getcwd()))

