import pandas as pd 
import datetime as dt 
import plotly
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

end = dt.datetime.now()
start = dt.datetime(2019,1,1)
interval = '1d'

st.title("Tracker")

stocklist = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA', 'JPM', 'JNJ', 'V', 'PG', 'HD', 'UNH', 'MA']
selected = st.selectbox("Select options", stocklist)

n_years = st.slider("Years of prediction:", 1, 5)
period = n_years * 365

@st.cache_data #Cache the data so it stores it
def load_data(ticker, start, end):
    df = yf.download(ticker, start, end)

    if df.empty:
        print(f"No data returned for {ticker}")
    else:
        df.index = pd.to_datetime(df.index).strftime('%d-%m-%Y')

    return df

data_loading = st.write("Loading")
data = load_data(selected, start, end)

st.subheader("Table with Info")
st.write(data.tail())

def plot_graph():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = data.index, y = data['Adj Close'], name = 'Price'))
    fig.layout.update(title_text = "Time Series Data",
                      xaxis_rangeslider_visible = True)
    st.plotly_chart(fig)

plot_graph()


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




