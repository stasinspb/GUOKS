import streamlit as st
import zipfile
import os
import shutil
import img2pdf
import xml.etree.cElementTree as ET
from pdfrw import PdfReader, PdfWriter



uploaded_zip = st.file_uploader("Загрузите ZIP-файл", type=["zip"])
if uploaded_zip is not None:
    zf = zipfile.ZipFile(uploaded_zip)
    if not os.path.exists('GUOKS'):
        os.makedirs('GUOKS')
    dir_path = os.path.join(os.getcwd(),'GUOKS')
    zf.extractall(dir_path)
    zf.close()

# for root, dirs, files in os.walk(dir_path):  # бежим по папкам
#     for a in dirs:
#         if a[:6] != 'GKUOKS' and a[:7] != 'Applied':  # ищем и удаляем все папки, которые не начинаются
#             shutil.rmtree(os.path.join(root, a))  # на GKUOKS или Applied, т.е. остаются только папки GKUOKS
#         else:
#             continue

# for root, dirs, files in os.walk(dir_path):  # снова бежим по папкам, удаляем sig, log, txt
#     for file in files:
#         if file.endswith('.sig') or \
#                 file.endswith('.log') or \
#                 file.endswith('.txt'):
#             os.remove(os.path.join(root, file))
                    
try:
    for root, dirs, files in os.walk(dir_path):                    # снова бежим по папкам, перекодируем имена файлов, если такое нужно
        for file in files:
            file_name = file.encode('cp437').decode('cp866')
            os.rename(os.path.join(root, file), os.path.join(root, file_name))
except:
    pass
#st.write(os.listdir(dir_path))

st.write(os.walk(dir_path))


for roots, dirs, files in os.walk(dir_path):
    st.write(dirs)
    for file in files:
        new_name = "noname"
        if file.endswith('.xml'):
            st.write(roots)
