# Dynamic TA-Lib Back-Test Script for Binance

import ccxt
import key_file as k
import pandas as pd
import matplotlib.pyplot as plt
import talib
import os

# Initialize Binance exchange
binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey': k.binance_api_key,
    'secret': k.binance_api_secret
})

initial_usdt_balance = 1000  # Starting balance in USDT
usd_per_trade = 100  # Amount in USD per trade

# Create a directory for backtests if it doesn't exist
output_dir = "backtests"
os.makedirs(output_dir, exist_ok=True)

def fetch_ohlcv(symbol, timeframe, since, until):
    """Fetch OHLCV data from Binance."""
    since_timestamp = binance.parse8601(since + 'T00:00:00Z')
    until_timestamp = binance.parse8601(until + 'T23:59:59Z')
    bars = binance.fetch_ohlcv(symbol, timeframe=timeframe, since=since_timestamp)
    
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    # Filter data within the specified date range
    df = df[(df['timestamp'] >= since) & (df['timestamp'] <= until)]
    
    return df

def calculate_indicator(df, indicator, period):
    """Calculate the specified TA-Lib indicator."""
    if indicator == 'SMA':
        df['indicator'] = talib.SMA(df['close'], timeperiod=period)
    elif indicator == 'EMA':
        df['indicator'] = talib.EMA(df['close'], timeperiod=period)
    elif indicator == 'RSI':
        df['indicator'] = talib.RSI(df['close'], timeperiod=period)
    elif indicator == 'VWAP':
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        df['cumulative_price_volume'] = (typical_price * df['volume']).cumsum()
        df['cumulative_volume'] = df['volume'].cumsum()
        df['indicator'] = df['cumulative_price_volume'] / df['cumulative_volume']
    else:
        raise ValueError(f"Unsupported indicator: {indicator}")
    return df

def generate_signals(df, indicator):
    """Generate trading signals based on the specified indicator."""
    df['signal'] = 0
    if indicator in ['SMA', 'EMA', 'VWAP']:
        df.loc[df['close'] > df['indicator'], 'signal'] = 1  # Buy signal
        df.loc[df['close'] < df['indicator'], 'signal'] = -1 # Sell signal
    elif indicator == 'RSI':
        df.loc[df['indicator'] < 30, 'signal'] = 1  # Buy signal
        df.loc[df['indicator'] > 70, 'signal'] = -1 # Sell signal
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

def backtest_indicator(symbol, timeframe, indicator, period, start_date, end_date):
    """Run the back-test for a given symbol, timeframe, indicator, and date range."""
    df = fetch_ohlcv(symbol, timeframe, start_date, end_date)
    df = calculate_indicator(df, indicator, period)
    df = generate_signals(df, indicator)
    df = simulate_trades(df, usd_per_trade, initial_usdt_balance)
    
    # Export to CSV
    csv_filename = os.path.join(output_dir, f'{indicator}_backtest_results_{symbol.replace("/", "_")}_{timeframe}_{start_date}_{end_date}.csv')
    df.to_csv(csv_filename, index=False)
    print(f'Back-test results exported to {csv_filename}')
    
    # Plot results
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot price and indicator in the first chart
    ax1.plot(df['timestamp'], df['close'], label='Close Price')
    ax1.plot(df['timestamp'], df['indicator'], label=indicator)
    
    # Plot buy signals
    buy_signals = df[df['signal'] == 1]
    ax1.plot(buy_signals['timestamp'], buy_signals['close'], '^', markersize=10, color='g', label='Buy Signal')
    
    # Plot sell signals
    sell_signals = df[df['signal'] == -1]
    ax1.plot(sell_signals['timestamp'], sell_signals['close'], 'v', markersize=10, color='r', label='Sell Signal')
    
    ax1.legend()
    ax1.set_title(f'{indicator} Back-Test Results for {symbol} ({timeframe})')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax1.grid()
    
    # Save the price and indicator chart
    plt_filename_price = os.path.join(output_dir, f'{indicator}_backtest_results_price_{symbol.replace("/", "_")}_{timeframe}_{start_date}_{end_date}.png')
    plt.savefig(plt_filename_price)
    print(f'Back-test price chart saved to {plt_filename_price}')
    
    # Plot total balance in a separate chart
    fig, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(df['timestamp'], df['total_balance'], label='Total Balance')
    ax2.legend()
    ax2.set_title(f'Balance Over Time for {symbol} ({timeframe})')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Total Balance')
    ax2.grid()
    
    # Save the balance chart
    plt_filename_balance = os.path.join(output_dir, f'{indicator}_backtest_results_balance_{symbol.replace("/", "_")}_{timeframe}_{start_date}_{end_date}.png')
    plt.savefig(plt_filename_balance)
    print(f'Back-test balance chart saved to {plt_filename_balance}')
    
    plt.show()

if __name__ == '__main__':
    # Example usage
    backtest_indicator('BTC/USDT', '1h', 'SMA', 20, '2024-06-01', '2024-06-30')
    backtest_indicator('ETH/USDT', '1h', 'EMA', 20, '2024-06-01', '2024-06-30')
    backtest_indicator('SOL/USDT', '1h', 'RSI', 14, '2024-06-01', '2024-06-30')
    backtest_indicator('BTC/USDT', '1h', 'VWAP', 20, '2024-06-01', '2024-06-30')
