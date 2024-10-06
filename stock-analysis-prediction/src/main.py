import pandas as pd 
import datetime as dt 
import plotly
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

st.title("Tracker")

page = st.sidebar.selectbox("Select Page", ['S&P 500 Analysis', 'Maritime Stocks & Commodities'])

stocklist = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA', 'JPM', 'JNJ', 'V', 'PG', 'HD', 'UNH', 'MA']

end = dt.datetime.now()
start = dt.datetime(2019,1,1)
start, end

@st.cache_data #Cache the data so it stores it
def load_data(ticker, start, end):
    df = yf.download(ticker, start, end)

    if df.empty:
        st.warning(f"No data returned for {ticker}")
    else:
        df.index = pd.to_datetime(df.index).strftime('%d-%m-%Y')

    return df

#Page 1: S&P 500 Analysis
if page == "S&P 500 Analysis":
    st.subheader("Top 15 S&P 500 Stock Analysis")
    
    selected = st.selectbox("Select options", stocklist)

    #Slider for number of years for prediction
    n_years = st.slider("Years of prediction:", 1, 5)
    period = n_years * 365
    
    #Load data for the selected stock
    data_loading = st.write("Loading")
    data = load_data(selected, start, end)
    
    st.subheader(f"Data for {selected}")
    st.write(data.tail())
    st.write("Data Loaded succesfully.")
    
    #Plotting the stock data
    def plot_graph():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = data.index, y = data['Adj Close'], name = 'Price'))
        fig.layout.update(title_text = "Time Series Data",
                      xaxis_rangeslider_visible = True)
        
        st.plotly_chart(fig)
        
    plot_graph()

#Page 2: Maritime Stocks & Commodities
elif page == "Maritime Stocks & Commodities":
    st.subheader("Maritime Stocks & Commodities")

    st.write("Coming soon: Monitor vessel companies and commodities")



# vessels = ['NIO', 'PYPL', 'META','TSLA', 'UBER', 'MANU', 
# 'NFLX', 'GC=F', 'SI=F', 'CL=F', 'ETH-USD', 'SHEL.L', 'BP', 'FRO', 'GLNG', 'TK', 
# 'GRAB', 'GOTO.JK', 'ZOMATO.NS', 'DHER.DE', '3690.HK', 'JMIA']

# # oil_gas = 

# # stocklist = 





