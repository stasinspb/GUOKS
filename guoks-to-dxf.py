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

def proverka_name(new_name):
    spisok = doc.layers
    s = new_name
    number = 1
    while s in spisok:
        number += 1
        s = new_name + " (" + str(number) + ")"
    return (s)
    
#--------------------------

st.write(uploaded_files.name)

if "processing_done" not in st.session_state:
    st.session_state.processing_done = False


st.write(os.listdir())
if os.path.exists('DXF'):
    shutil.rmtree(os.path.join(os.getcwd(),'DXF'))
st.write(os.listdir())
processing_done = False
st.title("Создание файла Autocad (dxf) из zip-архивов технических планов зданий и сооружений")
uploaded_files = st.file_uploader("Загрузите ZIP-файлы технических планов", type=["zip"], accept_multiple_files=True)

  
if uploaded_files is not None:
    doc = ezdxf.new(dxfversion="R2010")
    msp = doc.modelspace()
    cvet = 2
    os.makedirs('DXF')
    
    #---------------------------------------
    for uploaded_file in uploaded_files:
        if not os.path.exists(os.path.join(os.getcwd(),'DXF', uploaded_file.name)):
            os.makedirs(os.path.join(os.getcwd(),'DXF', uploaded_file.name))
        dir_path = os.path.join(os.getcwd(),'DXF', uploaded_file.name)
        extract_zip_with_directories(uploaded_file, dir_path)
    #---------------------------------------
    t = os.path.join(os.getcwd(),'DXF')
    for roots, dirs, files in os.walk(t):
        for file in files:
            if file.endswith('.xml'):
                name_oks = ""
                zd = False
                xml = os.path.join(roots, file)
                tree = ET.ElementTree(file=xml)
                root = tree.getroot()
                if root[0].tag == "Building":               ########### определяем здание или сооружение
                    zd = True
                if root.iter('NewConstruction') is not None:        ###### Определяем имя объекта для сооружений
                    for element in root.iter('NewConstruction'):
                        for el in element.iter('Name'):
                            name_oks = el.text
                if root.iter('NewBuilding') is not None:            ###### Определяем имя для зданий
                    for element in root.iter('NewBuilding'):
                        for el in element.iter('Name'):
                            name_oks = el.text
                if root.iter('NewUncompleted') is not None:         ###### Определяем имя для НЗС
                    for element in root.iter('NewUncompleted'):
                        for el in element.iter('Name'):
                            name_oks = el.text
                new_name_oks = name_oks.replace(chr(47), " ") \
                    .replace(chr(92), " ") \
                    .replace(chr(58), " ") \
                    .replace(chr(42), " ") \
                    .replace(chr(63), " ") \
                    .replace(chr(34), " ") \
                    .replace(chr(59), " ") \
                    .replace(chr(44), " ") \
                    .replace(chr(61), " ") \
                    .replace(chr(96), " ") \
                    .replace(">", "") \
                    .replace("<", "") \
                    .replace("|", "") \
                    .replace("Газопровод-отвод магистральный", "ГО") \
                    .replace("Газопровод-отвод", "ГО") \
                    .replace("газопровода-отвода магистрального", "ГО") \
                    .replace("Линия электропередачи", "ЛЭП") \
                    .replace(" Портовая", "") \
                    .replace("Подъездная автодорога", "Дорога")
                new_name_oks = proverka_name(new_name_oks)
                if zd is False:                                      ## создаем новый слой с именем объекта
                    doc.layers.add(new_name_oks, color=cvet)
                else:
                    doc.layers.add(new_name_oks, color=1)
                coord = []  ###### Определяем координаты объектов
                lst = []
                n_kontur = 0
                radius = '-'
                if root.iter('SpatialElement') is not None:
                     for element in root.iter('SpatialElement'):
                         points = []
                         for elem in element.iter('SpelementUnit'):
                             rad = 0
                             x = 0
                             y = 0
                             for el in elem.iter('Ordinate'):
                                 if 'R' not in el.attrib.keys():
                                     x = float(el.attrib['X'])
                                     y = float(el.attrib['Y'])
                                     points.append((y, x))
                             for el in elem.iter('Ordinate'):
                                 if 'R' in el.attrib.keys():
                                     x = float(el.attrib['X'])
                                     y = float(el.attrib['Y'])
                                     rad = float(el.attrib['R'])
                                     msp.add_circle((y, x), radius=rad, dxfattribs={"layer": new_name_oks})
                         if points != []:
                             msp.add_lwpolyline(points, dxfattribs={"layer": new_name_oks})
            cvet += 1
            if cvet == 50:
                cvet = 2
    doc.saveas(os.path.join(t, "Общий план объектов.dxf"))
    st.session_state.processing_done = True
    st.success("Обработка завершена!")
    with open(os.path.join(t, "Общий план объектов.dxf"), "rb") as file:
        if st.session_state.processing_done:
            st.download_button(
                label="Скачать dxf",
                data=file,
                file_name="Общий план объектов.dxf",
                mime="application/octet-stream")

                                 
                                     
                        
                            
                         
                
   
