# VWAP Back-Test Script for Binance

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

symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
timeframe = '1h'  # Hourly data
initial_usdt_balance = 1000  # Starting balance in USDT
usd_per_trade = 100  # Amount in USD per trade

def fetch_ohlcv(symbol, timeframe, since):
    """Fetch OHLCV data from Binance."""
    bars = binance.fetch_ohlcv(symbol, timeframe=timeframe, since=since)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def calculate_vwap(df):
    """Calculate the Volume Weighted Average Price (VWAP)."""
    df['cum_vol'] = df['volume'].cumsum()
    df['cum_vol_price'] = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum()
    df['vwap'] = df['cum_vol_price'] / df['cum_vol']
    return df

def generate_signals(df):
    """Generate trading signals based on VWAP."""
    df['signal'] = 0
    df.loc[df['close'] > df['vwap'], 'signal'] = 1  # Buy signal
    df.loc[df['close'] < df['vwap'], 'signal'] = -1 # Sell signal
    return df

def simulate_trades(df, usd_per_trade, initial_usdt_balance):
    """Simulate trades based on the signals."""
    balance_usdt = initial_usdt_balance  # Starting balance in USDT
    balance_btc = 0  # Starting balance in BTC (or ETH, or SOL)
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

def backtest_vwap(symbol):
    """Run the VWAP back-test for a given symbol."""
    since = binance.parse8601('2023-06-01T00:00:00Z')  # Fetch data from one month back
    df = fetch_ohlcv(symbol, timeframe, since)
    df = calculate_vwap(df)
    df = generate_signals(df)
    df = simulate_trades(df, usd_per_trade, initial_usdt_balance)
    
    # Export to CSV
    csv_filename = f'vwap_backtest_results_{symbol.replace("/", "_")}.csv'
    df.to_csv(csv_filename, index=False)
    print(f'Back-test results exported to {csv_filename}')
    
    # Plot results
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot price and VWAP in the first chart
    ax1.plot(df['timestamp'], df['close'], label='Close Price')
    ax1.plot(df['timestamp'], df['vwap'], label='VWAP')
    ax1.legend()
    ax1.set_title(f'VWAP Back-Test Results for {symbol}')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.grid()
    
    # Save the price and VWAP chart
    plt_filename_price = f'vwap_backtest_results_price_{symbol.replace("/", "_")}.png'
    plt.savefig(plt_filename_price)
    print(f'Back-test price chart saved to {plt_filename_price}')
    
    # Plot total balance in a separate chart
    fig, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(df['timestamp'], df['total_balance'], label='Total Balance')
    ax2.legend()
    ax2.set_title(f'Balance Over Time for {symbol}')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Total Balance')
    ax2.grid()
    
    # Save the balance chart
    plt_filename_balance = f'vwap_backtest_results_balance_{symbol.replace("/", "_")}.png'
    plt.savefig(plt_filename_balance)
    print(f'Back-test balance chart saved to {plt_filename_balance}')
    
    plt.show()

if __name__ == '__main__':
    for symbol in symbols:
        backtest_vwap(symbol)
