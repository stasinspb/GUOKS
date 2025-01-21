import streamlit as st
import zipfile
import os
#import shutil
#import xml.etree.cElementTree as ET

st.title("Создание файла Autocad (dxf) из zip-архивов технических планов зданий и сооружений")
uploaded_files = st.file_uploader("Загрузите ZIP-файлы технических планов", type=["zip"], accept_multiple_files=True)
for uploaded_file in uploaded_files:
    st.write(uploaded_file.name)
    if os.path.exists(uploaded_file.name):
        shutil.rmtree(os.path.join(os.getcwd(), uploaded_file.name))
    os.makedirs(uploaded_file.name)
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall(uploaded_file.name)
st.write(os.listdir())
