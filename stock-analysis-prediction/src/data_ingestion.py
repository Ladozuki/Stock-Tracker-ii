import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

def top_15_symbs():
    sp500 = yf.Ticker("^GSPC")
    #retrieves current constituents
    symbols = sp500.history(period = "1d").index.tolist()
    return symbols
    #function uses yfinance to get data for s&p 
    #makes code adaptable to changes in market


#Fetch stock data over the last 5 years 
def fetch_stock_prices(symbols: list, start_date: datetime):

    data = {}
    end_date = datetime.now().strftime('%Y-%m-%d')

    for symbol in symbols:
        stock = yf.Ticker(symbol)
        hist = stock.history(start = start_date.strftime('%Y-%m-%d'), end = end_date)
        data[symbol] = hist
    return data
    #function takes a list of symbols and a start date
    #stores data in a dictionay where keys are stock symbols and values are DF including hist price

def calculate_market_cap(data):
    market_cap_df = {}
    for symbol, df in data.items():

        market_cap = yf.Ticker(symbol).info['marketCap']
        market_cap_data[symbol] = market_cap

    return ranked = sorted(market_cap_df.items(), key = lambda x: x[1], reverse = True)[:15]
    #function retrieves its market cap and stores in dict 
    #sorts stock by market cap in descending order and returns top 15

#Save to postgresql
def save_to_db(data, db_config:dict, symbol: str, fetch_date: datetime):

    try:
        conn = psycopg2.conect(**db_conifg)
        cursor = conn.cursor()
        cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS top_15_stocks (
            id SERIAL PRIMARY KEY,
            stock_symbol VARCHAR (10) NOT NULL,
            ranking_date DATE NOT NULL,
            ranking_position INT NOT NOLL,
            pct_change DECIMAL (5, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

    for symbol, df in data.items():
        for date, row in df.iterrows():
            #get market cap data for symbol

            market_cap = get_cap(symbol)

            cursor.execute('''
                INSERT INTO top_15_stocks (symbol, date, open, high, low, close, volume, market_cap)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (symbol, date) DO NOTHING
            ''', (
                symbol,
                date.strftime ('%Y-%m-%d'),
                float(row['open']),
                float(row['high']),
                float(row['low']),
                float(row['close']),
                int(row['volume']),
                market_cap
                ))
                
        
    conn.commit()
    logging.info("Data saved to PostreSQL database.")
except Exception as e:
    logging.error(f"Failed to save data: {e}")

finally:
    if conn:
        conn.close()

