import streamlit as st
#import time
import requests
#import urllib3

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


response = requests.get(
    'https://httpbin.org/ip',
    verify=False,  # Отключение проверки SSL, если нужно
)
st.write(response.json())

