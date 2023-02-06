import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import json
import requests
import datetime
response = requests.get('https://api.coincap.io/v2/assets')
all_assets = {asset['symbol']: asset['id'] for asset in response.json()['data']}
asset_filter = st.sidebar.selectbox("Select the asset", list(all_assets.keys()))


url = f'https://api.coincap.io/v2/assets/{all_assets[asset_filter]}/history?interval=d1'
response = requests.get(url)
df_history = pd.DataFrame(response.json()['data'])
df_history.date = pd.to_datetime(df_history.date).dt.date
df_history.priceUsd = df_history.priceUsd.astype(float).round(decimals = 3)
layout = st.sidebar.columns([1, 1])
with layout[0]:
    start_date = st.date_input("Date from", value=df_history.date.values[0])
with layout[-1]:
    end_date = st.date_input("Date to", value=df_history.date.values[-1])

df_history = df_history[(df_history.date < end_date) & (df_history.date > start_date)]
df_history.date = df_history.date.astype(str)


st.bar_chart(data=df_history, x='date', y='priceUsd')
