import streamlit as st
import zipfile
import os

uploaded_zip = st.file_uploader("Загрузите ZIP-файл", type=["zip"])
if uploaded_zip is not None:
    zf = zipfile.ZipFile(uploaded_zip)
    os.makedirs('GUOKS')
    zf.extractall(os.path.join(os.getcwd(),'GUOKS'))
    zf.close()
st.success("Распаковано")
st.success(os.getcwd())
st.write(os.listdir(os.getcwd()))
st.write(os.listdir(os.path.join(os.getcwd(),'GUOKS')))

