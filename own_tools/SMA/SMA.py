# SMA Trading Bot for Binance

import ccxt
import key_file as k
import pandas as pd
import time

# Initialize Binance exchange
binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey': k.binance_api_key,
    'secret': k.binance_api_secret
})

symbol = 'BTC/USDT'
timeframe = '15m'
sma_period = 20
usd_amount = 1  # Amount in USD for the order size, must be greater than $5.00

def fetch_ohlcv(symbol, timeframe, limit=100):
    """Fetch OHLCV data from Binance."""
    bars = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def calculate_sma(df, period):
    """Calculate the Simple Moving Average (SMA)."""
    df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
    return df

def get_signal(df, sma_period):
    """Generate trading signal based on SMA."""
    latest_data = df.iloc[-1]
    if latest_data['close'] > latest_data[f'sma_{sma_period}']:
        return 'BUY'
    elif latest_data['close'] < latest_data[f'sma_{sma_period}']:
        return 'SELL'
    else:
        return 'HOLD'

def get_order_size(usd_amount):
    """Calculate the order size in BTC equivalent to the given USD amount."""
    ticker = binance.fetch_ticker(symbol)
    current_price = ticker['last']
    order_size = usd_amount / current_price
    return order_size

def check_balance():
    """Check the account balance for USDT."""
    balance = binance.fetch_balance()
    usdt_balance = balance['total']['USDT']
    return usdt_balance

def place_order(symbol, side, amount):
    """Place an order on Binance."""
    try:
        order = binance.create_market_order(symbol, side, amount)
        print(f'Order placed: {side} {amount} {symbol}')
        return order
    except ccxt.InsufficientFunds:
        print('Insufficient funds to place order.')
        return None

def run_bot():
    """Run the trading bot."""
    df = fetch_ohlcv(symbol, timeframe)
    df = calculate_sma(df, sma_period)
    signal = get_signal(df, sma_period)
    usdt_balance = check_balance()
    order_size = get_order_size(usd_amount)
    
    # Ensure there are enough funds to place the order
    if usdt_balance < usd_amount:
        print(f'Insufficient USDT balance to place order. Available balance: {usdt_balance}')
        return

    if signal == 'BUY':
        place_order(symbol, 'buy', order_size)
    elif signal == 'SELL':
        place_order(symbol, 'sell', order_size)
    else:
        print('No trading signal.')

if __name__ == '__main__':
    while True:
        run_bot()
        time.sleep(60 * 15)  # Run every 15 minutes
