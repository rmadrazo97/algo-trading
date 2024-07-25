# RSI Back-Test Script for Binance

import ccxt
import key_file as k
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import ta

# Initialize Binance exchange
binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey': k.binance_api_key,
    'secret': k.binance_api_secret
})

# Function to fetch historical data
def fetch_historical_data(symbol, timeframe, since):
    ohlcv = binance.fetch_ohlcv(symbol, timeframe, since=since)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Parameters
symbol = 'BTC/USDT'
timeframe = '1d'  # Daily data
since = binance.parse8601((datetime.utcnow() - timedelta(days=60)).isoformat())

# Fetch historical data for the last 2 months
df = fetch_historical_data(symbol, timeframe, since)

# Calculate RSI using the TA package
df['RSI'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()

# Backtest strategy
initial_balance_usdt = 1000
initial_balance_btc = 1000
balance_usdt = initial_balance_usdt
balance_btc = initial_balance_btc
btc_price = df['close'].iloc[0]
positions = []

for i in range(14, len(df)):
    if df['RSI'].iloc[i] < 30:  # Buy signal (RSI < 30)
        if balance_usdt >= 5:
            btc_amount = 5 / df['close'].iloc[i]
            balance_btc += btc_amount
            balance_usdt -= 5
            positions.append((df['timestamp'].iloc[i], 'Buy', df['close'].iloc[i], balance_usdt, balance_btc))
    elif df['RSI'].iloc[i] > 70:  # Sell signal (RSI > 70)
        if balance_btc * df['close'].iloc[i] >= 5:
            usdt_amount = 5
            btc_amount = 5 / df['close'].iloc[i]
            balance_btc -= btc_amount
            balance_usdt += usdt_amount
            positions.append((df['timestamp'].iloc[i], 'Sell', df['close'].iloc[i], balance_usdt, balance_btc))

# Create a DataFrame for positions
positions_df = pd.DataFrame(positions, columns=['timestamp', 'action', 'price', 'balance_usdt', 'balance_btc'])

# Add total balance (in USDT) column to positions DataFrame
positions_df['total_balance'] = positions_df['balance_usdt'] + positions_df['balance_btc'] * df['close'].iloc[-1]

# Save positions data to CSV
positions_df.to_csv('rsi_backtest_positions.csv', index=False)

# Plot the RSI and Bitcoin price with buy/sell signals
plt.figure(figsize=(14, 7))
plt.plot(df['timestamp'], df['close'], label='BTC/USDT Price', color='blue')
plt.plot(df['timestamp'], df['RSI'], label='RSI', color='orange')
for idx, row in positions_df.iterrows():
    if row['action'] == 'Buy':
        plt.scatter(row['timestamp'], row['price'], color='green', marker='^', label='Buy Signal' if idx == 0 else "")
    elif row['action'] == 'Sell':
        plt.scatter(row['timestamp'], row['price'], color='red', marker='v', label='Sell Signal' if idx == 0 else "")
plt.axhline(30, linestyle='--', color='red', alpha=0.5)
plt.axhline(70, linestyle='--', color='green', alpha=0.5)
plt.title('BTC/USDT Price and RSI with Buy/Sell Signals')
plt.xlabel('Date')
plt.ylabel('Price (USDT) / RSI')
plt.legend()
plt.savefig('rsi_btc_price_signals.png')
plt.show()

# Plot the balance change after each alert
plt.figure(figsize=(14, 7))
plt.plot(positions_df['timestamp'], positions_df['balance_usdt'], label='USDT Balance', color='green')
plt.plot(positions_df['timestamp'], positions_df['balance_btc'] * df['close'].iloc[-1], label='BTC Balance (in USDT)', color='blue')
plt.plot(positions_df['timestamp'], positions_df['total_balance'], label='Total Balance', color='purple')
plt.title('Balance Change After Each Buy/Sell Signal')
plt.xlabel('Date')
plt.ylabel('Balance (USDT)')
plt.legend()
plt.savefig('rsi_balance_change.png')
plt.show()
