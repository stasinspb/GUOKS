import streamlit as st
import zipfile
#import os
#import shutil
#import xml.etree.cElementTree as ET

st.title("Создание файла Autocad (dxf) из zip-архивов технических планов зданий и сооружений")
uploaded_files = st.file_uploader("Загрузите ZIP-файлы технических планов", type=["zip"], accept_multiple_files=True)
for uploaded_file in uploaded_files:
    st.write(uploaded_file.name)
