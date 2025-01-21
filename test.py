import streamlit as st
import os
st.write(os.listdir())
def reveal_button():
    st.session_state.show_button = True

# Устанавливаем начальное состояние
if "show_button" not in st.session_state:
    st.session_state.show_button = False

# Кнопка для события
st.button("Событие", on_click=reveal_button)

# Показываем кнопку после события
if st.session_state.show_button:
    st.button("Появившаяся кнопка")
