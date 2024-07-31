# VWMA Back-Test Script for Binance

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
vwma_period = 20  # Period for VWMA calculation
initial_usdt_balance = 1000  # Starting balance in USDT
usd_per_trade = 100  # Amount in USD per trade

def fetch_ohlcv(symbol, timeframe, since):
    """Fetch OHLCV data from Binance."""
    bars = binance.fetch_ohlcv(symbol, timeframe=timeframe, since=since)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def calculate_vwma(df, period):
    """Calculate the Volume Weighted Moving Average (VWMA)."""
    df['volXclose'] = df['volume'] * df['close']
    df['cum_vol'] = df['volume'].rolling(window=period).sum()
    df['cum_volXclose'] = df['volXclose'].rolling(window=period).sum()
    df['vwma'] = df['cum_volXclose'] / df['cum_vol']
    return df

def generate_signals(df):
    """Generate trading signals based on VWMA."""
    df['signal'] = 0
    df.loc[df['close'] > df['vwma'], 'signal'] = 1  # Buy signal
    df.loc[df['close'] < df['vwma'], 'signal'] = -1 # Sell signal
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

def backtest_vwma(symbol):
    """Run the VWMA back-test for a given symbol."""
    since = binance.parse8601('2023-06-01T00:00:00Z')  # Fetch data from one month back
    df = fetch_ohlcv(symbol, timeframe, since)
    df = calculate_vwma(df, vwma_period)
    df = generate_signals(df)
    df = simulate_trades(df, usd_per_trade, initial_usdt_balance)
    
    # Export to CSV
    csv_filename = f'vwma_backtest_results_{symbol.replace("/", "_")}.csv'
    df.to_csv(csv_filename, index=False)
    print(f'Back-test results exported to {csv_filename}')
    
    # Plot results
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot price and VWMA in the first chart
    ax1.plot(df['timestamp'], df['close'], label='Close Price')
    ax1.plot(df['timestamp'], df['vwma'], label='VWMA')
    ax1.legend()
    ax1.set_title(f'VWMA Back-Test Results for {symbol}')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.grid()
    
    # Save the price and VWMA chart
    plt_filename_price = f'vwma_backtest_results_price_{symbol.replace("/", "_")}.png'
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
    plt_filename_balance = f'vwma_backtest_results_balance_{symbol.replace("/", "_")}.png'
    plt.savefig(plt_filename_balance)
    print(f'Back-test balance chart saved to {plt_filename_balance}')
    
    plt.show()

if __name__ == '__main__':
    for symbol in symbols:
        backtest_vwma(symbol)
