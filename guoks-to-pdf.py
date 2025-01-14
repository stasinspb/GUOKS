import streamlit as st
import zipfile
import os
import shutil
import img2pdf
import xml.etree.cElementTree as ET
from pdfrw import PdfReader, PdfWriter


st.title("Создание pdf из zip-архива технического плана")
uploaded_zip = st.file_uploader("Загрузите ZIP-файл технического плана", type=["zip"])
if uploaded_zip is not None:
    zf = zipfile.ZipFile(uploaded_zip)
    if os.path.exists('GUOKS'):
        shutil.rmtree(os.path.join(os.getcwd(),'GUOKS'))
    os.makedirs('GUOKS')
    dir_path = os.path.join(os.getcwd(),'GUOKS')
    zf.extractall(dir_path)
    zf.close()

   
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
    
    
    #----------------------
    for roots, dirs, files in os.walk(dir_path):
        for file in files:
            new_name = "noname"
            if file.endswith('.xml'):
                my_files = os.listdir(os.path.join(roots, dirs[0]))
                #st.write(my_files)
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
                #st.write(geo)        
                for element in root.iter('SchemeDisposition'):      # ... по файлам схем ЗУ
                    try:
                        dis.append(element.attrib['Name'])
                    except:
                        for a in element:
                            dis.append(a.attrib['Name'])
                    finally:
                        pass 
                        
                for element in root.iter('DiagramContour'):         # ... по файлам с чертежами
                    try:
                        dia.append(element.attrib['Name'])
                    except:
                        for a in element:
                            dia.append(a.attrib['Name'])
                    finally:
                        pass
                        
                for my_file in my_files:
                    if my_file.endswith('.jpg'):
                        plans.append(my_file)
                        
                for element in root.iter('Appendix'):               # ... по файлам с приложениями, кроме файла с текстовой частью
                    for a in element:
                        if a[1].text != "Текстовая часть технического плана":
                           apps.append(a[2].attrib['Name'])
                #st.write(apps) 
    ########### начинаем собирать пдф ########################################
                #st.write(os.path.join(roots, dirs[0], text)) 
                reader_input = PdfReader(os.path.join(roots, dirs[0], text))    # начинаем с текстовой части
                writer_output = PdfWriter()
                for current_page in range(len(reader_input.pages)):
                    writer_output.addpage(reader_input.pages[current_page])
                #st.write("Текст добавлен")
                for p in geo:                                           # добавляем файлы с геодезией
                    #st.write(os.path.join(roots, p))
                    reader_input = PdfReader(os.path.join(roots, p).replace("\\","/"))
                    #st.write("Гео добавлен")
                    for current_page in range(len(reader_input.pages)):
                        writer_output.addpage(reader_input.pages[current_page])
    
                for p in dis:                                           # добавляем файлы со схемами ЗУ
                    reader_input = PdfReader(os.path.join(roots, p).replace("\\","/"))
                    for current_page in range(len(reader_input.pages)):
                        writer_output.addpage(reader_input.pages[current_page])
    
                for p in dia:                                           # добавляем файлы с чертежами
                    reader_input = PdfReader(os.path.join(roots, p).replace("\\","/"))
                    for current_page in range(len(reader_input.pages)):
                        writer_output.addpage(reader_input.pages[current_page])
    
                try:
                    for p in plans:                                           # добавляем файлы с поэтажками
                        pdf = img2pdf.convert(os.path.join(roots, p).replace("\\","/"))                       # создаем из картинки пдф
                        with open(os.path.join(roots, 'jpg-to-pdf.pdf'), 'wb') as f:
                            f.write(pdf)
                        reader_input = PdfReader(os.path.join(roots, 'jpg-to-pdf.pdf'))     # добавляем созданный пдф
                        for current_page in range(len(reader_input.pages)):
                            writer_output.addpage(reader_input.pages[current_page])
                except:
                    print("Не добавились поэтажные планы: - ", new_name)
    
                for p in apps:                                          # добавляем файлы приложений
                    reader_input = PdfReader(os.path.join(roots, p).replace("\\","/"))
                    for current_page in range(len(reader_input.pages)):
                        writer_output.addpage(reader_input.pages[current_page])
    
                writer_output.write(os.path.join(os.path.join(os.getcwd(), "Технический план.pdf"))) # сохраняем файл пдф
                st.write(new_name)
    
    #st.write(os.listdir(dir_path))
    with open(os.path.join(os.getcwd(), "Технический план.pdf"), "rb") as file:
        st.download_button(
            label="Скачать pdf",
            data=file,
            file_name="Технический план.pdf",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )



