import tempfile
import streamlit as st

uploaded_file = st.file_uploader("Загрузите ZIP-файл", type=["zip"])
with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    tmp_file = zipfile.ZipFile(file_path, 'r')
    tmp_file.close()
