import pandas as pd 
import datetime as dt 
import plotly
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu
from stocknews import StockNews
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
    prev_close = df['Adj Close'].iloc[-2]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = df['High'].max()
    low = df['Low'].min()
    volume = df['Volume'].mean()
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

#Navigation Bar
selected = option_menu(
    menu_title = None,
    options = ["Maritime Stocks & Commodities", "Market Watch"],
    icons = ['globe', 'speedometer2'],
    orientation = 'horizontal'
)

maritime_stocks = ['FRO', 'GLNG', 'TK', 'CL=F', 'BZ=F', 'STNG', 'GC=F', 'SI=F', 'SHEL.L', 'BP', 'TNP', 'NMM', 'EURN', 'SBLK', 'GSL', 
                   'DAC', 'CPLP', 'GOGL', 'LNG=F', 'HO=F', 'BCO=F', 'BDRY', 'NATGAS=F']

#Page 2: Maritime Stocks & Commodities
if selected == 'Maritime Stocks & Commodities':
    st.subheader("Maritime Stocks & Commodities")

    ticker = st.multiselect("Select Maritime Stocks: ", maritime_stocks)

    st.sidebar.header('Parameters')
    period = st.sidebar.radio('Select Time Period', ['1D', '1W', '1M', '3M', '6M', '1y', '5y'])
    end_date = dt.datetime.now()

        # Map the period to actual date ranges
    if period == "1D":
        start_date = end_date - pd.Timedelta(days=1)
    elif period == "1W":
        start_date = end_date - pd.Timedelta(weeks=1)
    elif period == "1M":
        start_date = end_date - pd.DateOffset(months=1)
    elif period == "3M":
        start_date = end_date - pd.DateOffset(months=3)
    elif period == "6M":
        start_date = end_date - pd.DateOffset(months=6)
    elif period == "1y":
        start_date = end_date - pd.DateOffset(years=1)
    elif period == "5y":
        start_date = end_date - pd.DateOffset(years=5)


    # Adding help text
    st.sidebar.markdown("### Technical Indicators")

    with st.expander("Indicator Overivew"):
        st.markdown("""
                            - **MA_20**: Smooths price data and identifies the direction of the trend.
                            - **MA_50**: Similar purpose  over a longer period, providing a clearer trend signal.
                            - **BB_Lower**: Indicates oversold conditions.
                            - **BB_Upper**: Indicates overbought conditions.
                            """)

    indicators = st.sidebar.multiselect('Technical Indicators', ['MA_20', 'MA_50'])
    
    #2B MAIN CONTENT AREA ####
    #Load data for the selected stock
    if ticker:
        for t in ticker:
            try:
                with st.spinner("Loading Data"):
                    data = load_data(t, start = start_date, end = end_date) #Display for each selected
                # data = calculate_metrics(data)
                    data = analysis(data)

                    last_close, prev_close, change, pct_change, high, low, volume = calculate_metrics(data)

                    st.write("Data Loaded succesfully.")

                    col1, col2, col3 = st.columns(3)
                    col1.metric(label = f"{ticker} Last Price", value = f"${last_close:.2f} ", delta = f"{change:.2f} ({pct_change:.2f}%)")
                    col2.metric("Low", f"${low:.2f}")
                    col3.metric("Volume", f"{int(volume):,}")

                    fig = px.line(data, x= data.index, y = data['Adj Close'])

                    for indicator in indicators:
                        if indicator == 'MA_20':
                            fig.add_trace(go.Scatter(x = data.index, y = data['MA_20'], name = '20-Day MA', line=dict(color = 'orange')))
                        elif indicator == 'MA_50':
                            fig.add_trace(go.Scatter(x = data.index, y = data['MA_50'], name = '50-Day MA', line=dict(color = 'green')))

                    #Format graph
                    fig.update_layout(#title_text = f"{ticker[0]} Time Series Data for with Moving Averages and Bollinger Bands",
                                    xaxis_title = 'Time',
                                    yaxis_title = 'Price(USD)')
                    
                    st.plotly_chart(fig, use_container_width = True)

                    sn = StockNews(ticker, save_news = False)
                    df_news = sn.read_rss()

                    with st.expander("News Section"):
                        for i in range(12):
                            st.subheader(f'News {i + 1}')
                            formatted_date = dt.datetime.strptime(df_news['published'][i], '%a, %d %b %Y %H:%M:%S %z').strftime('%d %b %Y')
                            st.write(f'{formatted_date}')
                            st.write(df_news['title'][i])
                            st.write(df_news['summary'][i])
                            

                    with st.expander("Historical Data"):
                        st.dataframe(data[['Adj Close', 'Volume', 'Open', 'Close']])

            except ValueError as e:
                st.error(e)

            with st.expander("View Recommendations"):
                recommendations = []
                st.write("\n No Immediate Action Recommended")

                    
            
stocklist = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA', 'JPM', 'JNJ', 'V', 'PG', 'HD', 'UNH', 'MA']

#TAB 1
#2A SIDEBAR FOR USER INPUT PARAMETERS
if selected == 'Market Watch':
    st.sidebar.header('Parameters')
    ticker = st.sidebar.multiselect("Select options", stocklist) #or .selectbox
    period = st.sidebar.radio('Select Time Period', ['1D', '1W', '1M', '3M', '6M', '1y', '5y'])
    end_date = dt.datetime.now()
    indicators = st.sidebar.multiselect('Technical Indicators', ['MA_20', 'MA_50', 'BB_Lower', 'BB_Upper'])

    st.subheader("Top 15 S&P 500 Stock Analysis")
    #2B MAIN CONTENT AREA ####

    # Map the period to actual date ranges
    if period == "1D":
        start_date = end_date - pd.Timedelta(days=1)
    elif period == "1W":
        start_date = end_date - pd.Timedelta(weeks=1)
    elif period == "1M":
        start_date = end_date - pd.DateOffset(months=1)
    elif period == "3M":
        start_date = end_date - pd.DateOffset(months=3)
    elif period == "6M":
        start_date = end_date - pd.DateOffset(months=6)
    elif period == "1y":
        start_date = end_date - pd.DateOffset(years=1)
    elif period == "5y":
        start_date = end_date - pd.DateOffset(years=5)


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

                col1, col2, col3 = st.columns(3)
                col1.metric(label = f"{ticker} Last Price", value = f"${last_close:.2f} ", delta = f"{change:.2f} ({pct_change:.2f}%)")
                col2.metric("Low", f"${low:.2f}")
                col3.metric("Volume", f"{int(volume):,}")

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
                fig.update_layout(#title_text = f"{ticker[0]} Time Series Data for with Moving Averages and Bollinger Bands",
                                xaxis_title = 'Time',
                                yaxis_title = 'Price(USD)')
                
                st.plotly_chart(fig, use_container_width = True)

                with st.expander("Historical Data"):
                    st.dataframe(data[['Adj Close', 'Volume', 'Open', 'Close']])

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


# vessels = ['NIO', 'PYPL', 'META','TSLA', 'UBER', 'MANU', 
# 'NFLX',  'CL=F', 'ETH-USD', , 'FRO', 'GLNG', 'TK', 
# 'GRAB', 'GOTO.JK', 'ZOMATO.NS', 'DHER.DE', '3690.HK', 'JMIA']

# oil_gas = 

# stocklist = 