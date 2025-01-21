import streamlit as st
import time

# Инициализация переменной состояния
if "processing_done" not in st.session_state:
    st.session_state.processing_done = False

# Эмуляция обработки файлов
if st.button("Начать обработку"):
    with st.spinner("Обработка файлов..."):
        time.sleep(3)  # Имитируем длительную обработку
        st.session_state.processing_done = True  # Сохраняем состояние в session_state
        st.success("Обработка завершена!")

# Показ кнопки "Скачать" только после завершения обработки
if st.session_state.processing_done:
    st.download_button(
        label="Скачать файл",
        data=b"Пример данных файла",  # Заглушка для данных файла
        file_name="example.dxf",
        mime="application/octet-stream",
    )

