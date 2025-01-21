import streamlit as st
import zipfile
import os
import shutil
import xml.etree.cElementTree as ET
import ezdxf
#--------------------------
def extract_zip_with_directories(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.infolist():
            fixed_path = member.filename.replace('\\', '/')
            target_path = os.path.join(extract_to, fixed_path)
            
            # Проверяем, является ли это папкой или файлом
            if member.is_dir():
                os.makedirs(target_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with open(target_path, 'wb') as f:
                    f.write(zip_ref.read(member.filename))

#--------------------------
doc = ezdxf.new(dxfversion="R2010")
msp = doc.modelspace()
cvet = 2

st.title("Создание файла Autocad (dxf) из zip-архивов технических планов зданий и сооружений")
uploaded_files = st.file_uploader("Загрузите ZIP-файлы технических планов", type=["zip"], accept_multiple_files=True)
if uploaded_files is not None:
    if os.path.exists('DXF'):
        shutil.rmtree(os.path.join(os.getcwd(),'DXF'))
    os.makedirs('DXF')
    
    #---------------------------------------
    for uploaded_file in uploaded_files:
        if not os.path.exists(os.path.join(os.getcwd(),'DXF', uploaded_file.name)):
            os.makedirs(os.path.join(os.getcwd(),'DXF', uploaded_file.name))
        dir_path = os.path.join(os.getcwd(),'DXF', uploaded_file.name)
        extract_zip_with_directories(uploaded_file, dir_path)
        st.write(os.listdir(dir_path))
    #---------------------------------------

   
   
