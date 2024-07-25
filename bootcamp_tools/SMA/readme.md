# README

## Overview

This Python script provides a comprehensive approach to cryptocurrency trading on the Phemex exchange using the CCXT library. It includes functionalities for managing open positions, fetching market data, implementing a kill switch, checking profit and loss (PnL), and calculating a Simple Moving Average (SMA) indicator for trading signals.

## Dependencies

Ensure you have the following Python libraries installed:

- `ccxt`: For interacting with cryptocurrency exchanges.
- `pandas`: For data manipulation.
- `schedule`: For task scheduling.
- `time`: For handling time-related tasks.

You can install the necessary libraries using the following command:
```bash
pip install ccxt pandas schedule
```

## Setup

Before running the script, make sure you have a `key_file.py` file with your Phemex API credentials defined as follows:
```python
xP_KEY = 'your_api_key'
xP_SECRET = 'your_secret_key'
```

## Code Explanation

### 1. Initialization

```python
import ccxt
import key_file as k
import time, schedule
import pandas as pd

phemex = ccxt.phemex({
    'enableRateLimit': True,
    'apiKey': k.xP_KEY,
    'secret': k.xP_SECRET
})
```
- Initializes the Phemex exchange with API credentials and rate limit enabled.

### 2. Global Variables

```python
symbol = 'uBTCUSD'
size = 1
bid = 29000
params = {'timeInForce': 'PostOnly',}
```
- Defines the trading symbol, order size, initial bid price, and order parameters.

### 3. Functions

#### a. `open_positions(symbol=symbol)`
- Fetches open positions for a given symbol and returns relevant position details including position side, size, and status.

#### b. `ask_bid(symbol=symbol)`
- Fetches the current ask and bid prices for the given symbol.
- Returns the ask price, bid price, and order book data.

#### c. `kill_switch(symbol=symbol)`
- Implements a kill switch to close open positions based on current market conditions.
- Cancels all open orders and places limit orders to close the position.
- Rechecks the position status and ensures it is closed.

#### d. `pnl_close(symbol=symbol, target=target, max_loss=max_loss)`
- Monitors positions for their PnL and closes the position when a target profit or stop loss is reached.
- Calls the kill switch to close the position based on PnL.

#### e. `size_kill()`
- Ensures the position size does not exceed the maximum risk threshold and activates the kill switch if necessary.

#### f. `df_sma(symbol=symbol, timeframe='15m', limit=100, sma=20)`
- Calculates the Simple Moving Average (SMA) for the given symbol over a specified timeframe.
- Determines trading signals (BUY or SELL) based on the SMA and current bid price.
- Returns a DataFrame with the SMA and trading signals.

### 4. Main Execution Flow

The main flow of the script is managed through function calls, which can be scheduled or triggered based on market conditions.

### Example Usage

- To fetch open positions:
  ```python
  open_positions(symbol='uBTCUSD')
  ```

- To check the ask and bid prices:
  ```python
  ask_bid(symbol='uBTCUSD')
  ```

- To activate the kill switch:
  ```python
  kill_switch(symbol='uBTCUSD')
  ```

- To check PnL and potentially close positions:
  ```python
  pnl_close(symbol='uBTCUSD', target=9, max_loss=-8)
  ```

- To perform a size kill check:
  ```python
  size_kill()
  ```

- To calculate SMA and generate trading signals:
  ```python
  df_sma(symbol='uBTCUSD', timeframe='15m', limit=100, sma=20)
  ```

### Running the Script

To run the script, simply execute the Python file:
```bash
python your_script_name.py
```

## Notes

- Ensure that your API keys are securely stored and not hard-coded directly in the script.
- Modify the parameters such as `symbol`, `target`, `max_loss`, `timeframe`, and `sma` as per your trading strategy and risk management policies.
- The script uses basic print statements for logging. For a production environment, consider using a more robust logging framework.
- Thoroughly test the script in a controlled environment or with minimal real funds before deploying it with significant capital.

This script provides a framework for automated trading with risk management features and technical analysis using the SMA indicator. Ensure thorough testing and customization based on your trading strategy and risk tolerance.