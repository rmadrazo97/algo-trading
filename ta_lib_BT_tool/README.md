# TA-Lib Back-Test Script

## Overview

This script performs back-tests on various technical indicators using TA-Lib for cryptocurrency trading on Binance. It dynamically accepts parameters for the symbol, timeframe, indicator, period, and date range. The results, including CSV files and charts, are stored in a dedicated `backtests` folder for organized storage.

## Prerequisites

Ensure you have the following Python libraries installed:
```bash
pip install ccxt pandas matplotlib TA-Lib
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
import talib
import os
```

### Parameters

The script defines several parameters for the back-test:
```python
initial_usdt_balance = 1000  # Starting balance in USDT
usd_per_trade = 100  # Amount in USD per trade
output_dir = "backtests"
os.makedirs(output_dir, exist_ok=True)
```

### Functions

1. **fetch_ohlcv(symbol, timeframe, since, until)**:
   Fetch historical OHLCV data from Binance within the specified date range.

2. **calculate_indicator(df, indicator, period)**:
   Calculate the specified TA-Lib indicator (SMA, EMA, RSI, or VWAP).

3. **generate_signals(df, indicator)**:
   Generate buy and sell signals based on the specified indicator.

4. **simulate_trades(df, usd_per_trade, initial_usdt_balance)**:
   Simulate trades based on the generated signals, starting with a balance of $1000 USDT. Trades are executed with $100 per trade.

5. **backtest_indicator(symbol, timeframe, indicator, period, start_date, end_date)**:
   Run the back-test for the specified symbol, timeframe, indicator, and date range. Export results to CSV and plot the back-test results.

### Running the Back-Test

To run the back-test, use the following example commands:

```python
if __name__ == '__main__':
    # Example usage
    backtest_indicator('BTC/USDT', '1h', 'SMA', 20, '2024-06-01', '2024-06-30')
    backtest_indicator('ETH/USDT', '1h', 'EMA', 20, '2024-06-01', '2024-06-30')
    backtest_indicator('SOL/USDT', '1h', 'RSI', 14, '2024-06-01', '2024-06-30')
    backtest_indicator('BTC/USDT', '1h', 'VWAP', 20, '2024-06-01', '2024-06-30')
```

### Output

1. **CSV Files**:
   - The results are exported to CSV files in the `backtests` folder. The filenames follow the pattern: `{indicator}_backtest_results_{symbol}_{timeframe}_{start_date}_{end_date}.csv`.

2. **Charts**:
   - The script generates two types of charts:
     - **Price and Indicator Chart**: Displays the price, indicator, buy signals, and sell signals.
     - **Balance Chart**: Displays the total balance over time.
   - The charts are saved in the `backtests` folder. The filenames follow the pattern: `{indicator}_backtest_results_price_{symbol}_{timeframe}_{start_date}_{end_date}.png` and `{indicator}_backtest_results_balance_{symbol}_{timeframe}_{start_date}_{end_date}.png`.

### Example Output

1. **CSV File**:
   - `backtests/SMA_backtest_results_BTC_USDT_1h_2024-06-01_2024-06-30.csv`
   - `backtests/EMA_backtest_results_ETH_USDT_1h_2024-06-01_2024-06-30.csv`
   - `backtests/RSI_backtest_results_SOL_USDT_1h_2024-06-01_2024-06-30.csv`
   - `backtests/VWAP_backtest_results_BTC_USDT_1h_2024-06-01_2024-06-30.csv`

2. **Charts**:
   - `backtests/SMA_backtest_results_price_BTC_USDT_1h_2024-06-01_2024-06-30.png`
   - `backtests/SMA_backtest_results_balance_BTC_USDT_1h_2024-06-01_2024-06-30.png`
   - `backtests/EMA_backtest_results_price_ETH_USDT_1h_2024-06-01_2024-06-30.png`
   - `backtests/EMA_backtest_results_balance_ETH_USDT_1h_2024-06-01_2024-06-30.png`
   - `backtests/RSI_backtest_results_price_SOL_USDT_1h_2024-06-01_2024-06-30.png`
   - `backtests/RSI_backtest_results_balance_SOL_USDT_1h_2024-06-01_2024-06-30.png`
   - `backtests/VWAP_backtest_results_price_BTC_USDT_1h_2024-06-01_2024-06-30.png`
   - `backtests/VWAP_backtest_results_balance_BTC_USDT_1h_2024-06-01_2024-06-30.png`

### Notes

- Ensure that your Binance API keys are securely stored in the `key_file.py`.
- Adjust the `timeframe`, `initial_usdt_balance`, and `usd_per_trade` parameters based on your requirements.
- Thoroughly test the script with a small amount of funds or in a paper trading environment before using it with significant capital.

This script provides a framework for back-testing various TA-Lib indicators on different trading pairs and timeframes. Customize and expand it according to your trading strategy and risk tolerance.