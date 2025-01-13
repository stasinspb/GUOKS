import streamlit as st
import os
import zipfile
import shutil
import xml.etree.cElementTree as ET
from pdfrw import PdfReader, PdfWriter
import img2pdf

st.title("Печать технического плана")

# Загрузка файла
uploaded_file = st.file_uploader("Загрузите файл GUOKS....zip", type=["zip"])

if uploaded_file is not None:
    st.success("Файл успешно загружен!")
temp_dir = "temp_folder"
os.makedirs(temp_dir)
with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)
st.title("архив распакован")
