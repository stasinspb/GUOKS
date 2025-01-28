import streamlit as st
import time
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


cookies = {
    '_ym_uid': '1710416513250114214',
    '_ym_d': '1735209875',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
}
headers = {
    "connection": "keep-alive",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://nspd.gov.ru/map?zoom=13.145350990199525&coordinate_x=4013445.434014521&coordinate_y=8464174.616664883&theme_id=1&is_copy_url=true&active_layers=%E8%B3%90',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

proxies = {
    "https": "87.249.6.137:8082"
}

paramsEX = {
    'thematicSearchId': '1',
    'query': '89:04:020602:1337',
}
st.write("1")
response = requests.get(
    'https://nspd.gov.ru/api/geoportal/v2/search/geoportal',
    params=paramsEX,
    cookies=cookies,
    headers=headers,
    verify=False,
    proxies=proxies,
)

st.write(response.json())


