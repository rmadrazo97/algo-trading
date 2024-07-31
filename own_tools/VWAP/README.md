# VWAP Back-Test Script

## Overview

This script performs a back-test of a Volume-Weighted Average Price (VWAP) trading strategy on Binance for BTC/USDT, ETH/USDT, and SOL/USDT trading pairs. It fetches historical OHLCV (Open, High, Low, Close, Volume) data, calculates VWAP, generates trading signals, simulates trades, and exports the results to CSV files. The script also generates separate charts for price/VWAP and account balance over time.

## Prerequisites

Ensure you have the following Python libraries installed:
```bash
pip install ccxt pandas matplotlib
```

You also need to create a `key_file.py` containing your Binance API credentials:
```python
# key_file.py
binance_api_key = 'your_api_key'
binance_api_secret = 'your_api_secret'
```

## Script Details

### Dependencies

The script imports necessary libraries and initializes the Binance exchange connection using the `ccxt` library:
```python
import ccxt
import key_file as k
import pandas as pd
import matplotlib.pyplot as plt

binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey': k.binance_api_key,
    'secret': k.binance_api_secret
})
```

### Parameters

The script defines several parameters for the back-test:
```python
symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
timeframe = '1h'  # Hourly data
initial_usdt_balance = 1000  # Starting balance in USDT
usd_per_trade = 100  # Amount in USD per trade
```

### Functions

1. **fetch_ohlcv(symbol, timeframe, since)**:
   Fetch historical OHLCV data from Binance.
2. **calculate_vwap(df)**:
   Calculate the Volume Weighted Average Price (VWAP).
3. **generate_signals(df)**:
   Generate buy and sell signals based on the VWAP.
4. **simulate_trades(df, usd_per_trade, initial_usdt_balance)**:
   Simulate trades based on the generated signals, starting with a balance of $1000 USDT. Trades are executed with $100 per trade.
5. **backtest_vwap(symbol)**:
   Run the back-test for the specified symbol, export results to a CSV file, and plot the back-test results.

### Running the Back-Test

The main section of the script runs the back-test for each symbol:
```python
if __name__ == '__main__':
    for symbol in symbols:
        backtest_vwap(symbol)
```

### Output

1. **CSV Files**:
   - `vwap_backtest_results_<symbol>.csv`: Contains the historical data, VWAP, signals, and simulated balances.

2. **Charts**:
   - `vwap_backtest_results_price_<symbol>.png`: Chart showing the close price and VWAP.
   - `vwap_backtest_results_balance_<symbol>.png`: Chart showing the total balance over time.

## How to Run

To run the back-test, execute the script:
```bash
python vwap_backtest.py
```

### Example Output

1. **CSV File**:
   - `vwap_backtest_results_BTC_USDT.csv`
   - `vwap_backtest_results_ETH_USDT.csv`
   - `vwap_backtest_results_SOL_USDT.csv`

2. **Charts**:
   - `vwap_backtest_results_price_BTC_USDT.png`
   - `vwap_backtest_results_balance_BTC_USDT.png`
   - `vwap_backtest_results_price_ETH_USDT.png`
   - `vwap_backtest_results_balance_ETH_USDT.png`
   - `vwap_backtest_results_price_SOL_USDT.png`
   - `vwap_backtest_results_balance_SOL_USDT.png`

These outputs provide insights into the performance of the VWAP trading strategy over the specified period.

## Notes

- Ensure that your Binance API keys are securely stored in the `key_file.py`.
- Adjust the `timeframe`, `initial_usdt_balance`, and `usd_per_trade` parameters based on your requirements.
- Thoroughly test the script with a small amount of funds or in a paper trading environment before using it with significant capital.

This script provides a framework for back-testing the VWAP trading strategy on multiple trading pairs. Customize and expand it according to your trading strategy and risk tolerance.