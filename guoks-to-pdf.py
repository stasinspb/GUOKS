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
                    
try:
    for root, dirs, files in os.walk(dir_path):                    # снова бежим по папкам, перекодируем имена файлов, если такое нужно
        for file in files:
            file_name = file.encode('cp437').decode('cp866')
            os.rename(os.path.join(root, file), os.path.join(root, file_name))
except:
    pass

my_files = os.listdir(dir_path)
st.write(my_files)

#----------------------
for roots, dirs, files in os.walk(dir_path):
    for file in files:
        new_name = "noname"
        if file.endswith('.xml'):
            geo = []        # назначаем массивы для файлов с геодезией
            dis = []        # со схемами ЗУ
            dia = []        # с чертежами
            plans = []      # с поэтажками
            apps = []       # с приложениями
            zd = False
            text = ""                       # определяем имя файла с текстовой частью ТП
            for my_file in my_files:
                if "TextPart" in my_file:
                    text = my_file

            #st.write(text)
    
    
            ############  работа с xml ################
            xml = os.path.join(roots, file)
            st.write(os.path.join(roots, file))
            tree = ET.ElementTree(file=xml)
            root = tree.getroot()
            for elem1 in root.iter('Package'):
                for elem2 in elem1[0]:
                    if elem2.tag == 'Name':
                        new_name = elem2.text
                        break
                    for elem3 in elem2:
                        if elem3.tag == 'Name':
                            new_name = elem3.text
                            
            for element in root.iter('SchemeGeodesicPlotting'):     # заполняем массивы с именами файлов по геодезии
                try:
                    geo.append(element.attrib['Name'])
                except:
                    for a in element:
                        geo.append(a.attrib['Name'])
                finally:
                    pass
            st.write(geo)        
            for element in root.iter('SchemeDisposition'):      # ... по файлам схем ЗУ
                try:
                    dis.append(element.attrib['Name'])
                except:
                    for a in element:
                        dis.append(a.attrib['Name'])
                finally:
                    pass
            st.write(dis) 
            for element in root.iter('DiagramContour'):         # ... по файлам с чертежами
                try:
                    dia.append(element.attrib['Name'])
                except:
                    for a in element:
                        dia.append(a.attrib['Name'])
                finally:
                    pass
            st.write(dia)        
            for my_file in my_files:
                if my_file.endswith('.jpg'):
                    plans.append(my_file)
            st.write(plans)
            for element in root.iter('Appendix'):               # ... по файлам с приложениями, кроме файла с текстовой частью
                for a in element:
                    if a[1].text != "Текстовая часть технического плана":
                       apps.append(a[2].attrib['Name'])
            st.write(apps)
########### начинаем собирать пдф ########################################



