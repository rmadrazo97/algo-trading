# RSI Back-Test Script for Bitcoin Trading

## Overview

This project demonstrates how to use the Relative Strength Index (RSI) indicator to back-test a trading strategy on Bitcoin (BTC) using historical data from Binance. The script calculates the RSI, identifies buy and sell signals based on the RSI values, and plots the results. It also exports the trade data and balance changes to a CSV file and saves the generated charts.

## Relative Strength Index (RSI)

The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. It is typically used to identify overbought or oversold conditions in a market.

- **RSI Formula**: The RSI is calculated using the formula:
  \[
  RSI = 100 - \left( \frac{100}{1 + RS} \right)
  \]
  where \( RS \) (Relative Strength) is the average gain of up periods divided by the average loss of down periods over a specified time frame (typically 14 periods).

- **Interpretation**:
  - **Overbought**: RSI > 70, suggesting that the asset may be overbought and a price correction could occur.
  - **Oversold**: RSI < 30, suggesting that the asset may be oversold and a price increase could occur.

## Strategy

1. **Buy Signal**: When the RSI falls below 30, indicating that the asset is oversold.
2. **Sell Signal**: When the RSI rises above 70, indicating that the asset is overbought.

## Files

- `rsi_backtest.py`: The main script that performs the back-test.
- `rsi_backtest_positions.csv`: The CSV file containing the details of each trade and balance changes.
- `rsi_btc_price_signals.png`: The chart showing BTC price, RSI, and buy/sell signals.
- `rsi_balance_change.png`: The chart showing the change in balance over time.

## How to Run the Script

1. **Install Dependencies**:
   Ensure you have the necessary Python packages installed:
   ```sh
   pip install ccxt pandas matplotlib ta
   ```

2. **Configure API Keys**:
   Create a `key_file.py` and include your Binance API keys:
   ```python
   binance_api_key = 'your_binance_api_key'
   binance_api_secret = 'your_binance_api_secret'
   ```

3. **Run the Script**:
   Execute the script to perform the back-test and generate charts:
   ```sh
   python rsi_backtest.py
   ```

## Script Details

### Initialization and Data Fetching

- The script initializes a connection to the Binance exchange using the `ccxt` library.
- It fetches historical BTC/USDT data for the past 60 days using the `fetch_historical_data` function.

### RSI Calculation

- The RSI is calculated using the `RSIIndicator` function from the `ta` package with a 14-day window.

### Backtesting

- The script starts with an initial balance of $1000 USDT and $1000 worth of BTC.
- It iterates through the data, applying the buy and sell rules based on the RSI values.
- Balances are adjusted accordingly, and trade details are recorded.

### Plotting

- The script plots the BTC price along with RSI values, highlighting buy and sell signals.
- It also plots the balance changes, including the total balance (sum of USDT and BTC value).
- The charts are saved as `rsi_btc_price_signals.png` and `rsi_balance_change.png`.

### CSV Export

- Trade details and balance changes are exported to `rsi_backtest_positions.csv` for further analysis.

## Results

- **Trade Signals**: The script identifies and marks the buy and sell signals on the BTC price chart.
- **Balance Changes**: The balance changes after each trade are plotted, providing a visual representation of the strategy's performance.

## Conclusion

This project provides a practical example of using the RSI indicator for trading Bitcoin. By following this guide, you can understand the implementation details and analyze the strategy's effectiveness through the generated charts and CSV file.