import streamlit as st
import zipfile
import os
import shutil

uploaded_zip = st.file_uploader("Загрузите ZIP-файл", type=["zip"])
if uploaded_zip is not None:
    zf = zipfile.ZipFile(uploaded_zip)
    os.mkdir('GUOKS')
    dir_path = os.path.join(os.getcwd(),'GUOKS')
    zf.extractall(dir_path)
    zf.close()

#st.success("Распаковано")
#st.success(os.getcwd())
#st.write(os.listdir(os.getcwd()))
#st.write(os.listdir(os.path.join(os.getcwd(),'GUOKS')))

st.write(os.listdir(dir_path))

for root, dirs, files in os.walk(dir_path):  # бежим по папкам
    for a in dirs:
        if a[:6] != 'GKUOKS' and a[:7] != 'Applied':  # ищем и удаляем все папки, которые не начинаются
            shutil.rmtree(os.path.join(root, a))  # на GKUOKS или Applied, т.е. остаются только папки GKUOKS
        else:
            continue

for root, dirs, files in os.walk(dir_path):  # снова бежим по папкам, удаляем sig, log, txt
    for file in files:
        if file.endswith('.sig') or \
                file.endswith('.log') or \
                file.endswith('.txt'):
            os.remove(os.path.join(root, file))
                    
st.write(os.listdir(dir_path))
