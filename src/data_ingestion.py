import yfinance as yf
import pandas as pd
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
import json
import os
import sys
from datetime import datetime, timedelta

def load_tickers():
    tickers = set(['SPY', '^VIX'])
    if os.path.exists('portfolio.csv'):
        df_p = pd.read_csv('portfolio.csv')
        tickers.update(df_p[df_p['Type'] == 'Equity']['Ticker'].tolist())
    if os.path.exists('watchlist.csv'):
        df_w = pd.read_csv('watchlist.csv')
        tickers.update(df_w['Ticker'].tolist())
    return list(tickers)

def get_market_regime(spy_price, spy_200sma, vix_close):
    if spy_price > spy_200sma and vix_close > 20:
        return "Bull Volatile"
    elif spy_price > spy_200sma and vix_close <= 20:
        return "Bull Quiet"
    elif spy_price <= spy_200sma and vix_close > 25:
        return "Bear Volatile"
    elif spy_price <= spy_200sma and vix_close <= 25:
        return "Bear Quiet"
    return "Unknown"

def fetch_data():
    tickers = load_tickers()
    market_data = {}
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365) # 1 year data for 200 SMA

    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        try:
            df = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)
            
            if df.empty:
                continue
                
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Calculate Technicals using ta
            df['SMA_20'] = SMAIndicator(close=df['Close'], window=20).sma_indicator()
            df['SMA_50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
            df['SMA_200'] = SMAIndicator(close=df['Close'], window=200).sma_indicator()
            df['RSI_14'] = RSIIndicator(close=df['Close'], window=14).rsi()
            
            macd = MACD(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)
            df['MACD_12_26_9'] = macd.macd()
            df['MACDs_12_26_9'] = macd.macd_signal()
            df['MACDh_12_26_9'] = macd.macd_diff()
            
            bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
            df['BBL_20_2.0'] = bb.bollinger_lband()
            df['BBU_20_2.0'] = bb.bollinger_hband()
            
            # Drop NaN rows which are at the beginning due to MAs
            df = df.dropna()
            if df.empty:
                continue

            latest = df.iloc[-1]
            
            def get_val(col_name):
                val = latest.get(col_name, 0)
                if isinstance(val, pd.Series):
                    return float(val.iloc[0])
                return float(val)

            ticker_data = {
                'close': get_val('Close'),
                'volume': get_val('Volume'),
                'sma_20': get_val('SMA_20'),
                'sma_50': get_val('SMA_50'),
                'sma_200': get_val('SMA_200'),
                'rsi_14': get_val('RSI_14'),
                'macd': get_val('MACD_12_26_9'),
                'macd_signal': get_val('MACDs_12_26_9'),
                'macd_hist': get_val('MACDh_12_26_9'),
                'bb_lower': get_val('BBL_20_2.0'),
                'bb_upper': get_val('BBU_20_2.0'),
            }
            
            # Fetch News
            t = yf.Ticker(ticker)
            news = t.news
            if news:
                ticker_data['news'] = [n.get('title', '') for n in news[:3]]
            else:
                ticker_data['news'] = []
            
            market_data[ticker] = ticker_data
            
        except Exception as e:
            print(f"Error fetching {ticker}: {e}", file=sys.stderr)

    # Determine Regime
    regime = "Unknown"
    if 'SPY' in market_data and '^VIX' in market_data:
        spy_close = market_data['SPY']['close']
        spy_200 = market_data['SPY']['sma_200']
        vix_close = market_data['^VIX']['close']
        regime = get_market_regime(spy_close, spy_200, vix_close)
        
    output = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'regime': regime,
        'data': market_data
    }
    
    os.makedirs('data', exist_ok=True)
    with open('data/market_context.json', 'w') as f:
        json.dump(output, f, indent=4)
        
    print("Market data fetched and saved to data/market_context.json")

if __name__ == "__main__":
    fetch_data()