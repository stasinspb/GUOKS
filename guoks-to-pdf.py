import os
import zipfile
import shutil
import xml.etree.ElementTree as ET
from pdfrw import PdfReader, PdfWriter
import img2pdf
import streamlit as st

def process_folder(input_folder):
    folder_list = [name for name in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, name))]
    
    for folder in folder_list:
        folder_path = os.path.join(input_folder, folder)
        
        # Обрабатываем ZIP архивы
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.zip'):  # ищем zip архивы
                    z = zipfile.ZipFile(os.path.join(root, file), 'r')
                    zip_folder = os.path.join(folder_path, file[:-4])
                    os.makedirs(zip_folder, exist_ok=True)
                    z.extractall(zip_folder)  # распаковываем в созданную папку
                    z.close()

        # Убираем лишние папки
        for root, dirs, files in os.walk(folder_path):
            for dir_name in dirs:
                if dir_name[:6] != 'GKUOKS' and dir_name[:7] != 'Applied':  
                    shutil.rmtree(os.path.join(root, dir_name))  # удаляем ненужные папки

        # Удаляем ненужные файлы
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.sig') or file.endswith('.log') or file.endswith('.txt'):
                    os.remove(os.path.join(root, file))

        try:
            # Переименовываем файлы в кодировке
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_name = file.encode('cp437').decode('cp866')
                    os.rename(os.path.join(root, file), os.path.join(root, file_name))
        except Exception as e:
            st.warning(f"Ошибка при переименовании файлов: {e}")

        # Обрабатываем XML файлы
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.xml'):
                    process_xml_file(os.path.join(root, file), dirs, root, folder_path)


def process_xml_file(xml_path, dirs, roots, folder_path):
    my_files = os.listdir(os.path.join(roots, dirs[0]))  # список файлов в папке 'Applied_files'
    
    geo = []  # геодезия
    dis = []  # схемы ЗУ
    dia = []  # чертежи
    plans = []  # поэтажные планы
    apps = []  # приложения
    zd = False
    text = ""  # текстовая часть ТП

    for my_file in my_files:
        if my_file[:4] == 'Text':
            text = my_file

    # Работа с XML для получения имени объекта
    tree = ET.ElementTree(file=xml_path)
    root = tree.getroot()

    if root[0].tag == "Construction":
        zd = False
    if root[0].tag == "Building" or root[0].tag == "Flat":
        zd = True

    new_name = "noname"
    for elem1 in root.iter('Package'):
        for elem2 in elem1[0]:
            if elem2.tag == 'Name':
                new_name = elem2.text
                break
            for elem3 in elem2:
                if elem3.tag == 'Name':
                    new_name = elem3.text

    # Сбор файлов для разных частей плана
    for element in root.iter('SchemeGeodesicPlotting'):
        geo.append(element.attrib['Name'] if 'Name' in element.attrib else [a.attrib['Name'] for a in element])

    for element in root.iter('SchemeDisposition'):
        dis.append(element.attrib['Name'] if 'Name' in element.attrib else [a.attrib['Name'] for a in element])

    for element in root.iter('DiagramContour'):
        dia.append(element.attrib['Name'] if 'Name' in element.attrib else [a.attrib['Name'] for a in element])

    if zd:
        for my_file in my_files:
            if my_file.endswith('.jpg'):
                plans.append(my_file)

    for element in root.iter('Appendix'):
        for a in element:
            if a[1].text != "Текстовая часть технического плана":
                apps.append(a[2].attrib['Name'])

    # Генерация PDF
    reader_input = PdfReader(os.path.join(roots, dirs[0], text))
    writer_output = PdfWriter()

    for current_page in range(len(reader_input.pages)):
        writer_output.addpage(reader_input.pages[current_page])

    for p in geo:
        reader_input = PdfReader(os.path.join(roots, p))
        for current_page in range(len(reader_input.pages)):
            writer_output.addpage(reader_input.pages[current_page])

    for p in dis:
        reader_input = PdfReader(os.path.join(roots, p))
        for current_page in range(len(reader_input.pages)):
            writer_output.addpage(reader_input.pages[current_page])

    for p in dia:
        reader_input = PdfReader(os.path.join(roots, p))
        for current_page in range(len(reader_input.pages)):
            writer_output.addpage(reader_input.pages[current_page])

    try:
        for p in plans:
            pdf = img2pdf.convert(os.path.join(roots, dirs[0], p))  # создаем из картинки пдф
            with open(os.path.join(roots, dirs[0], 'jpg-to-pdf.pdf'), 'wb') as f:
                f.write(pdf)
            reader_input = PdfReader(os.path.join(roots, dirs[0], 'jpg-to-pdf.pdf'))
            for current_page in range(len(reader_input.pages)):
                writer_output.addpage(reader_input.pages[current_page])
    except Exception as e:
        st.warning(f"Не добавились поэтажные планы для {new_name}: {e}")

    for p in apps:
        reader_input = PdfReader(os.path.join(roots, p))
        for current_page in range(len(reader_input.pages)):
            writer_output.addpage(reader_input.pages[current_page])

    output_pdf_path = os.path.join(folder_path, f"{new_name}_Технический_план.pdf")
    writer_output.write(output_pdf_path)
    st.success(f"PDF файл успешно сохранен: {output_pdf_path}")


# Интерфейс Streamlit
st.title('Преобразование XML в PDF')

input_folder = st.text_input('Укажите путь к папке с объектами:')
if input_folder:
    if os.path.isdir(input_folder):
        process_folder(input_folder)
    else:
        st.error("Указанный путь не является директорией.")
