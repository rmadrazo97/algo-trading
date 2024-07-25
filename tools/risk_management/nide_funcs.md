# README

## Overview

This Python script provides various functions for managing cryptocurrency trades on the Hyper Liquid platform. It includes functionalities to fetch market data, place and manage orders, check account balances, and implement risk management through a kill switch and PnL (Profit and Loss) close.

## Dependencies

Ensure you have the following Python libraries installed:

- `dontshare`: Custom library for sensitive information like private keys (imported as `d`).
- `nice_funcs`: Custom library for utility functions (imported as `n`).
- `eth_account`: For handling Ethereum accounts.
- `hyperliquid`: For interacting with Hyper Liquid's API.
- `ccxt`: For interacting with cryptocurrency exchanges.
- `pandas`: For data manipulation.
- `schedule`: For task scheduling.
- `requests`: For making HTTP requests.

You can install the necessary libraries using the following command:
```bash
pip install eth_account hyperliquid ccxt pandas schedule requests
```

## Setup

Before running the script, make sure you have the following:

1. **Private Key**: Your Ethereum account private key stored in `dontshare.py` as `private_key`.
2. **Utility Functions**: The `nice_funcs` module should contain the necessary utility functions like `pnl_close`, `acct_bal`, and `kill_switch`.

## Code Explanation

### 1. Initialization

```python
import dontshare as d 
import nice_funcs as n 
from eth_account.signers.local import LocalAccount
import eth_account 
import json 
import time 
from hyperliquid.info import Info 
from hyperliquid.exchange import Exchange 
from hyperliquid.utils import constants 
import ccxt 
import pandas as pd 
import datetime 
import schedule 
import requests 
```
- Imports necessary libraries and custom modules for handling Ethereum accounts, interacting with Hyper Liquid API, and other utilities.

### 2. Global Variables

```python
symbol='WIF'
```
- Defines the trading symbol.

### 3. Functions

#### a. `ask_bid(symbol)`
- Fetches the ask and bid prices for the given symbol.
- Returns the ask price, bid price, and level 2 market data.

#### b. `get_sz_px_decimals(coin)`
- Retrieves size and price decimals for the given coin.
- Returns the size decimals and price decimals.

#### c. `limit_order(coin, is_buy, sz, limit_px, reduce_only, account)`
- Places a limit order (buy or sell) for the given coin.
- Rounds the size to the appropriate decimal places and prints order details.
- Returns the order result.

#### d. `acct_bal(account)`
- Fetches and prints the current account value.
- Returns the account value.

#### e. `get_position(symbol, account)`
- Retrieves the current position information for the given symbol.
- Returns position details including size, entry price, PnL percentage, and position direction (long/short).

#### f. `cancel_all_orders(account)`
- Cancels all open orders for the account.
- Prints the open orders and cancels each one.

#### g. `kill_switch(symbol, account)`
- Implements a kill switch to close open positions based on the current market conditions.
- Cancels all open orders and places limit orders to close the position.
- Rechecks the position status and ensures it is closed.

#### h. `pnl_close(symbol, target, max_loss, account)`
- Monitors positions for their PnL and closes the position when a target profit or stop loss is reached.
- Calls the kill switch to close the position based on PnL.

### Example Usage

- To fetch ask and bid prices:
  ```python
  ask, bid, l2_data = ask_bid(symbol='WIF')
  ```

- To place a limit order:
  ```python
  order_result = limit_order('WIF', True, 10, 5000, False, account)
  ```

- To check account balance:
  ```python
  account_value = acct_bal(account)
  ```

- To get current position:
  ```python
  position_details = get_position('WIF', account)
  ```

- To cancel all open orders:
  ```python
  cancel_all_orders(account)
  ```

- To activate the kill switch:
  ```python
  kill_switch('WIF', account)
  ```

- To check PnL and potentially close positions:
  ```python
  pnl_close('WIF', 4, -5, account)
  ```

## Notes

- Ensure that your private key is securely stored and not hard-coded directly in the script.
- The script uses basic print statements for logging. For a production environment, consider using a more robust logging framework.
- Thoroughly test the script in a controlled environment or with minimal real funds before deploying it with significant capital.

This script provides a framework for automated trading with risk management features for the Hyper Liquid platform. Ensure thorough testing and customization based on your trading strategy and risk tolerance.