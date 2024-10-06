import pandas as pd 
import datetime as dt 
import matplotlib.pyplot as plt 
import plotly
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
import yfinance as yf

# end = dt.datetime.now()
# start = dt.datetime(2019,1,1)
# interval = '1d'

# stocklist = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA', 'JPM', 'JNJ', 'V', 'PG', 'HD', 'UNH', 'MA']

# vessels = ['NIO', 'PYPL', 'META','TSLA', 'UBER', 'MANU', 
# 'NFLX', 'GC=F', 'SI=F', 'CL=F', 'ETH-USD', 'SHEL.L', 'BP', 'FRO', 'GLNG', 'TK', 
# 'GRAB', 'GOTO.JK', 'ZOMATO.NS', 'DHER.DE', '3690.HK', 'JMIA']

# # oil_gas = 

# # stocklist = 


# df = yf.download(stocklist, start, end, interval = interval)

# if df.empty:
#     print(f"No data returned for ")
# else: 

#     df.index = pd.to_datetime(df.index).strftime('%d-%m-%Y')

st.title("Price Tracker")

st.write("""
## Explore various prices
""")

