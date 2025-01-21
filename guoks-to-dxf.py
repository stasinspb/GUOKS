import streamlit as st
import zipfile
import os
import shutil
#import xml.etree.cElementTree as ET

# for file in os.listdir():
#     if file not in [".git", "guoks-to-dxf.py", "requirements.txt", ".streamlit", "guoks-to-pdf.py"]:
#         shutil.rmtree(os.path.join(os.getcwd(), file))
    
# st.write(os.listdir())

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


st.title("Создание файла Autocad (dxf) из zip-архивов технических планов зданий и сооружений")
uploaded_files = st.file_uploader("Загрузите ZIP-файлы технических планов", type=["zip"], accept_multiple_files=True)

if uploaded_files is not None:
    if os.path.exists('DXF'):
        shutil.rmtree(os.path.join(os.getcwd(),'DXF'))
    os.makedirs('DXF')
    for uploaded_file in uploaded_files:
        os.makedirs(os.path.join(os.getcwd(), 'DXF', uploaded_file.name))
        dir_path = os.path.join(os.getcwd(),'GUOKS', uploaded_file.name)
        #---------------------------------------
        extract_zip_with_directories(uploaded_file, dir_path)
        #---------------------------------------

for root, dirs, files in os.walk('GUOKS'): 
    for file in files:
        st.write(file)
try:
    shutil.rmtree(os.path.join(os.getcwd(),'GUOKS'))
except:
    pass
# st.write(os.listdir())
# os.remove("GKUOKS_0cc7df6c-a687-4556-94d4-0cb4df49abf9.xml.sig")
# st.write(os.listdir())

# for uploaded_file in uploaded_files:
#     st.write(uploaded_file.name)
#     if os.path.exists(uploaded_file.name):
#         shutil.rmtree(os.path.join(os.getcwd(), uploaded_file.name))
#     #os.makedirs(uploaded_file.name)
#     #with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
#         #zip_ref.extractall(uploaded_file.name)
# st.write(os.listdir())
