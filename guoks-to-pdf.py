import os
import zipfile
import shutil
import xml.etree.cElementTree as ET
import PyPDF2
import img2pdf
import streamlit as st

def process_files(file_path):
    # Проверяем, существует ли путь
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден!")

    dir_path = os.path.dirname(file_path)

    # Распаковка zip-файла
    with zipfile.ZipFile(file_path, 'r') as z:
        z.extractall(dir_path)

    # Удаляем ненужные папки
    for root, dirs, files in os.walk(dir_path):
        for a in dirs:
            if a[:6] != 'GKUOKS' and a[:7] != 'Applied':
                shutil.rmtree(os.path.join(root, a))

    # Удаляем ненужные файлы
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(('.sig', '.log', '.txt')):
                os.remove(os.path.join(root, file))

    # Перекодируем имена файлов
    try:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_name = file.encode('cp437').decode('cp866')
                os.rename(os.path.join(root, file), os.path.join(root, file_name))
    except Exception as e:
        st.error(f"Ошибка при перекодировке имен файлов: {e}")

    # Обработка файлов XML и создание PDF
    for roots, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.xml'):
                return process_xml(roots, dirs, file, dir_path)

def process_xml(roots, dirs, file, dir_path):
    new_name = "noname"
    my_files = os.listdir(os.path.join(roots, dirs[0]))

    geo = []        # файлы геодезии
    dis = []        # схемы ЗУ
    dia = []        # чертежи
    plans = []      # поэтажные планы
    apps = []       # приложения
    zd = False
    text = ""       # текстовая часть ТП

    for my_file in my_files:
        if my_file[:4] == 'Text':
            text = my_file

    # Работа с XML
    xml = os.path.join(roots, file)
    tree = ET.ElementTree(file=xml)
    root = tree.getroot()

    if root[0].tag in ["Building", "Flat"]:
        zd = True

    for elem1 in root.iter('Package'):
        for elem2 in elem1[0]:
            if elem2.tag == 'Name':
                new_name = elem2.text
                break
            for elem3 in elem2:
                if elem3.tag == 'Name':
                    new_name = elem3.text

    for element in root.iter('SchemeGeodesicPlotting'):
        geo.append(element.attrib.get('Name', ''))

    for element in root.iter('SchemeDisposition'):
        dis.append(element.attrib.get('Name', ''))

    for element in root.iter('DiagramContour'):
        dia.append(element.attrib.get('Name', ''))

    if zd:
        for my_file in my_files:
            if my_file.endswith('.jpg'):
                plans.append(my_file)

    for element in root.iter('Appendix'):
        for a in element:
            if a[1].text != "Текстовая часть технического плана":
                apps.append(a[2].attrib['Name'])

    # Создание PDF с использованием PyPDF2
    pdf_writer = PyPDF2.PdfWriter()

    # Текстовая часть ТП
    with open(os.path.join(roots, dirs[0], text), "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            pdf_writer.add_page(page)

    # Геодезия
    for p in geo:
        with open(os.path.join(roots, p), "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                pdf_writer.add_page(page)

    # Схемы ЗУ
    for p in dis:
        with open(os.path.join(roots, p), "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                pdf_writer.add_page(page)

    # Черчежи
    for p in dia:
        with open(os.path.join(roots, p), "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                pdf_writer.add_page(page)

    # Поэтажные планы
    try:
        for p in plans:
            pdf_data = img2pdf.convert(os.path.join(roots, dirs[0], p))
            with open(os.path.join(roots, dirs[0], 'jpg-to-pdf.pdf'), 'wb') as f:
                f.write(pdf_data)
            with open(os.path.join(roots, dirs[0], 'jpg-to-pdf.pdf'), "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    pdf_writer.add_page(page)
    except:
        st.warning("Не добавились поэтажные планы.")

    # Приложения
    for p in apps:
        with open(os.path.join(roots, p), "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                pdf_writer.add_page(page)

    # Сохраняем финальный PDF
    output_pdf_path = os.path.join(dir_path, "Технический план.pdf")
    with open(output_pdf_path, "wb") as f:
        pdf_writer.write(f)

    # Возвращаем путь к PDF
    return output_pdf_path

# Streamlit интерфейс
st.title("Процесс обработки ZIP-файлов и создания PDF")

uploaded_file = st.file_uploader("Загрузите ZIP-файл", type=["zip"])

if uploaded_file is not None:
    # Сохраняем файл локально
    save_path = "./uploaded_file.zip"
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write("Обработка файла...")

    try:
        # Процесс обработки
        pdf_path = process_files(save_path)
        st.success(f"Файл успешно обработан! Скачайте PDF: {pdf_path}")

        # Ссылка для скачивания
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Скачать PDF",
                data=f,
                file_name="Технический_план.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Произошла ошибка: {e}")
