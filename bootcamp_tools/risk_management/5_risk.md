# README

## Overview

This Python script is designed for managing risk in cryptocurrency trading using the Phemex exchange through the `ccxt` library. The script includes functions for opening positions, fetching order book details, implementing a kill switch for open positions, checking profit and loss (PnL), and managing position sizes.

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
params = {'timeInForce': 'PostOnly'}
```
- Defines the trading symbol, order size, initial bid price, and order parameters.

### 3. Functions

#### a. `open_positions()`
- Fetches open positions for a given symbol and returns relevant position details.

#### b. `ask_bid()`
- Fetches and prints the current ask and bid prices for the given symbol.

#### c. `kill_switch()`
- Implements a kill switch to close open positions based on current market conditions.

#### d. `pnl_close()`
- Checks whether the profit or loss target has been met and initiates the kill switch if necessary.

#### e. `size_kill()`
- Ensures the position size does not exceed the maximum risk threshold and activates the kill switch if necessary.

### 4. Main Execution Flow

The main flow of the script is managed through function calls, which are scheduled or triggered based on market conditions.

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

## Notes

- Ensure that your API keys are securely stored and not hard-coded directly in the script.
- Modify the `symbol`, `target`, `max_loss`, and other parameters as per your trading strategy and risk management policies.
- The script uses basic print statements for logging. For a production environment, consider using a more robust logging framework.

This script provides a framework for automated trading with risk management features. Ensure thorough testing with paper trading or minimal real funds before deploying it with significant capital.