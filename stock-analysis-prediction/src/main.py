import pandas as pd 
import datetime as dt 
import plotly
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import yfinance as yf
  

# Define functions for pulling, processing and creating technical indicators
def load_data(ticker, start, end):

    df = yf.download(ticker, start, end)

    if df.empty:
        raise ValueError(f"No data fetched for ticker: {ticker}")
    
    df.index = pd.to_datetime(df.index).strftime('%d-%m-%Y')

    # df = df[['Adj Close', 'Volume']]

    return df


def calculate_metrics(df):
    last_close = df['Adj Close'].iloc[-1]
    prev_close = df['Adj Close'].iloc[0]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = df['High'].max()
    low = df['Low'].min()
    volume = df['Volume'].sum()
    return last_close, prev_close, change, pct_change, high, low, volume

def analysis(df):
    #Calculate Moving Averages
    df[('MA_20')] = df[('Adj Close')].rolling(window=20).mean()
    df[('MA_50')] = df[('Adj Close')].rolling(window=50).mean()

    #Calculate Bollinger Bands
    df['Upper Band'] = df[('MA_20')] + (df[('Adj Close')].rolling(window=20).std() * 2)
    df['Lower Band'] = df[('MA_50')] - (df[('Adj Close')].rolling(window=20).std() * 2)

    return df


end = dt.datetime.now()
start = dt.datetime(2019,1,1)

#CREATING DASHBOARD FOR APP LAYOUT

#Set up page layout
st.set_page_config(layout = "wide")
st.header("Tracking Dashboard")
#Tab seperation
tab1, tab2 = st.tabs(["SP5", "Maritime Stocks & Commodities"])

stocklist = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA', 'JPM', 'JNJ', 'V', 'PG', 'HD', 'UNH', 'MA']

#TAB 1
#2A SIDEBAR FOR USER INPUT PARAMETERS
with tab1: 
    st.sidebar.header('Parameters')
    ticker = st.sidebar.multiselect("Select options", stocklist) #or .selectbox
    start_date = st.sidebar.date_input('Start')
    end_date = st.sidebar.date_input('End')
    indicators = st.sidebar.multiselect('Technical Indicators', ['MA_20', 'MA_50', 'BB_Lower', 'BB_Upper'])

    st.subheader("Top 15 S&P 500 Stock Analysis")

    
    #2B MAIN CONTENT AREA ####
    #Load data for the selected stock
    if ticker:
        try:
            with st.spinner("Loading Data"):
                data = load_data(ticker, start = start_date, end = end_date) #Display for each selected
            # data = calculate_metrics(data)
                data = analysis(data)

                last_close, prev_close, change, pct_change, high, low, volume = calculate_metrics(data)

                st.write("Data Loaded succesfully.")

                st.sidebar.metric(label = f"{ticker} Last Price", value = f"${last_close:.2f} ", delta = f"{change:.2f} ({pct_change:.2f}%)")

                col1, col2 = st.columns(2)
                col1.metric("Low", f"${low:.2f}")
                col2.metric("Volume", f"{volume:,}")

                fig = px.line(data, x= data.index, y = data['Adj Close'])

                for indicator in indicators:
                    if indicator == 'MA_20':
                        fig.add_trace(go.Scatter(x = data.index, y = data['MA_20'], name = '20-Day MA', line=dict(color = 'orange')))
                    elif indicator == 'MA_50':
                        fig.add_trace(go.Scatter(x = data.index, y = data['MA_50'], name = '50-Day MA', line=dict(color = 'green')))
                    elif indicator == 'BB_Upper':
                        fig.add_trace(go.Scatter(x = data.index, y = data['Upper Band'], name = 'Upper B', line=dict(color = 'red')))
                    elif indicator == 'BB_Lower':
                        fig.add_trace(go.Scatter(x = data.index, y = data['Lower Band'], name = 'Lower B', line=dict(color = 'lightgray')))

                #Format graph
                fig.update_layout(title_text = f"{ticker[0]} Time Series Data for with Moving Averages and Bollinger Bands",
                                xaxis_title = 'Time',
                                yaxis_title = 'Price(USD)')
                
                st.plotly_chart(fig, use_container_width = True)

                with st.expander("Historical Data"):
                    st.dataframe(data[['Adj Close', 'Volume']])

        except ValueError as e:
            st.error(e)

            

    # if ticker:
    #     for stock in ticker:
    #         data = load_data(stock, start, end)
    #         if data is not None:
    #             data = analysis(data)
    #             plot_graph(data)

                # #Calculate RSI
                # delta = df['Adj Close'].diff()
                # gain = (delta.where(delta > 0, 0)).rolling(window = 14).mean()
                # loss = (-delta.where(delta < 0, 0)).rolling(window = 14).mean()
                # rs = gain / loss
                # df['RSI'] = 100 - (100 / (1 + rs.fillna(0)))

                # st.subheader("RSI Analysis")
                # rsi_fig = go.Figure()
                # rsi_fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI', line=dict(color='purple')))
                # rsi_fig.add_hline(y=70, line=dict(color='red', dash='dash'), name='Overbought')
                # rsi_fig.add_hline(y=30, line=dict(color='green', dash='dash'), name='Oversold')
                # rsi_fig.layout.update(title_text="RSI Indicator", xaxis_title="Date", yaxis_title="RSI")

                # st.plotly_chart(rsi_fig)

        with st.expander("View Recommendations"):
            recommendations = []
                    
            st.write("\n No Immediate Action Recommended")

maritime_stocks = ['FRO', 'GLNG', 'TK', 'STNG', 'TNP', 'NMM', 'EURN', 'SBLK', 'GSL', 
                   'DAC', 'CPLP', 'GOGL', 'CL=F', 'LNG=F', 'HO=F', 'BCO=F', 'BDRY', 'NATGAS=F']

#Page 2: Maritime Stocks & Commodities
with tab2:
    st.header("Maritime Stocks & Commodities")
    st.write("Monitor vessel companies and commodities")

    selected_maritime = st.multiselect("Select Maritime Stocks: ", maritime_stocks)

    # #Load data for selected maritime stock data 
    # if selected_maritime:
    #     maritime_data = {}
    #     for stock in selected_maritime:
    #         maritime_data[stock] = load_data(stock, start, end)

    #     for stock, data in maritime_data.items():
    #         st.subheader(f"Data for {stock}")
    #         st.write(data.tail(30))
    #         st.write("Data Loaded Successfully.")

    #         #Plotting the maritime stock data
    #         fig = go.Figure()
    #         fig.add_trace(go.Scatter(x = data.index, y = data['Adj Close'], name = 'Price', line=dict(color = 'blue')))
    #         fig.add_trace(go.Scatter(x = data.index, y = data['MA_20'], name = '20-Day MA', line=dict(color = 'orange')))
    #         fig.add_trace(go.Scatter(x = data.index, y = data['MA_50'], name = '50-Day MA', line=dict(color = 'green')))

    #         fig.layout.update(title_text = f"{stock} Time Series Data",
    #                           xaxis_rangeslider_visible = True)
    #         st.plotly_chart(fig)

    #         # Recommendations for maritime stocks
    #         with st.expander(f"Recommendations for {stock}"):
    #             recommendations = []
    #             if data['RSI'].iloc[-1] < 30:
    #                 recommendations.append("Oversold: Consider Buying.")
    #             elif data['RSI'].iloc[-1] > 70:
    #                 recommendations.append("Overbought: Consider Selling.")
    #             else:
    #                 recommendations.append("No immediate action recommended.")
    #             st.write("\n".join(recommendations))


# vessels = ['NIO', 'PYPL', 'META','TSLA', 'UBER', 'MANU', 
# 'NFLX', 'GC=F', 'SI=F', 'CL=F', 'ETH-USD', 'SHEL.L', 'BP', 'FRO', 'GLNG', 'TK', 
# 'GRAB', 'GOTO.JK', 'ZOMATO.NS', 'DHER.DE', '3690.HK', 'JMIA']

# # oil_gas = 

# # stocklist = 





