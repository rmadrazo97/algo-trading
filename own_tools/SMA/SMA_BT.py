# SMA Back-Test Script for Binance

import ccxt
import key_file as k
import pandas as pd
import matplotlib.pyplot as plt

# Initialize Binance exchange
binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey': k.binance_api_key,
    'secret': k.binance_api_secret
})

symbol = 'BTC/USDT'
timeframe = '1h'  # Hourly data
sma_period = 20
initial_usdt_balance = 500  # Starting balance in USDT
initial_btc_balance = 0.01  # Starting balance in BTC (approx. $500 worth at $50,000/BTC)
usd_per_trade = 5  # Amount in USD per trade

def fetch_ohlcv(symbol, timeframe, since):
    """Fetch OHLCV data from Binance."""
    bars = binance.fetch_ohlcv(symbol, timeframe=timeframe, since=since)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def calculate_sma(df, period):
    """Calculate the Simple Moving Average (SMA)."""
    df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
    return df

def generate_signals(df, sma_period):
    """Generate trading signals based on SMA."""
    df['signal'] = 0
    df.loc[df['close'] > df[f'sma_{sma_period}'], 'signal'] = 1  # Buy signal
    df.loc[df['close'] < df[f'sma_{sma_period}'], 'signal'] = -1 # Sell signal
    return df

def simulate_trades(df, usd_per_trade):
    """Simulate trades based on the signals."""
    balance_usdt = initial_usdt_balance  # Starting balance in USDT
    balance_btc = initial_btc_balance  # Starting balance in BTC
    df['balance_usdt'] = balance_usdt
    df['balance_btc'] = balance_btc

    for i in range(1, len(df)):
        if df.loc[i, 'signal'] == 1 and df.loc[i-1, 'signal'] != 1:  # Buy signal
            btc_to_buy = usd_per_trade / df.loc[i, 'close']
            if balance_usdt >= usd_per_trade:
                balance_btc += btc_to_buy
                balance_usdt -= usd_per_trade
        elif df.loc[i, 'signal'] == -1 and df.loc[i-1, 'signal'] != -1:  # Sell signal
            usdt_to_sell = balance_btc * df.loc[i, 'close']
            balance_usdt += usdt_to_sell
            balance_btc = 0

        df.loc[i, 'balance_usdt'] = balance_usdt
        df.loc[i, 'balance_btc'] = balance_btc

    df['total_balance'] = df['balance_usdt'] + df['balance_btc'] * df['close']
    return df

def backtest_sma():
    """Run the SMA back-test."""
    since = binance.parse8601('2023-06-01T00:00:00Z')  # Fetch data from one month back
    df = fetch_ohlcv(symbol, timeframe, since)
    df = calculate_sma(df, sma_period)
    df = generate_signals(df, sma_period)
    df = simulate_trades(df, usd_per_trade)
    
    # Export to CSV
    df.to_csv('sma_backtest_results.csv', index=False)
    print('Back-test results exported to sma_backtest_results.csv')
    
    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['close'], label='Close Price')
    plt.plot(df['timestamp'], df[f'sma_{sma_period}'], label=f'SMA {sma_period}')
    plt.plot(df['timestamp'], df['total_balance'], label='Total Balance')
    plt.legend()
    plt.title('SMA Back-Test Results')
    plt.xlabel('Date')
    plt.ylabel('Price / Balance')
    plt.grid()
    plt.savefig('sma_backtest_results.png')
    print('Back-test chart saved to sma_backtest_results.png')
    plt.show()

if __name__ == '__main__':
    backtest_sma()
