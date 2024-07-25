# README

## Overview

This Python script demonstrates how to build a kill switch and PnL (Profit and Loss) close for Hyper Liquid trading. The script manages trading risk by monitoring the account balance and implementing automated trade closures based on predefined profit and loss targets.

## Dependencies

Ensure you have the following Python libraries installed:

- `nice_funcs`: Custom library for utility functions (imported as `n`).
- `dontshare`: Custom library for sensitive information like private keys (imported as `d`).
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
import nice_funcs as n 
import dontshare as d 
from eth_account.signers.local import LocalAccount 
import eth_account 
import json, time 
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
symbol = 'WIF'
max_loss = -5
target = 4 
acct_min = 9 
timeframe = '4h'
size = 10 
coin = symbol 
secret_key = d.private_key
account = LocalAccount = eth_account.Account.from_key(secret_key)
acct_min = 7 
```
- Defines various parameters for trading, including the symbol, maximum loss, target profit, account minimum balance, trading timeframe, and order size.
- Retrieves the private key from the `dontshare` module and initializes the Ethereum account.

### 3. Main Function: `bot()`

```python
def bot():
    print('this is our bot')
    print('controlling risk with our pnl close')

    # check pnl close
    n.pnl_close(symbol, target, max_loss, account)

    # if my account size goes under $100, and never $70
    acct_val = float(n.acct_bal(account))

    if acct_val < acct_min:
        print(f'account value is {acct_val} and closing because out low is {acct_min}')
        n.kill_switch(symbol, account)
```
- Defines the `bot()` function that controls risk by checking PnL and account balance.
- Calls `n.pnl_close` to check if the profit or loss target has been reached.
- Checks the account balance using `n.acct_bal` and activates the kill switch using `n.kill_switch` if the balance falls below the predefined minimum.

### 4. Execution

```python
bot()
```
- Executes the `bot()` function.

## Usage

- Ensure that your private key and utility functions are correctly set up in `dontshare.py` and `nice_funcs.py`, respectively.
- Modify the parameters such as `symbol`, `max_loss`, `target`, `acct_min`, and `size` as per your trading strategy and risk management policies.
- Run the script using the following command:
```bash
python your_script_name.py
```

## Notes

- Ensure that your private key is securely stored and not hard-coded directly in the script.
- The script uses basic print statements for logging. For a production environment, consider using a more robust logging framework.
- Thoroughly test the script in a controlled environment or with minimal real funds before deploying it with significant capital.

This script provides a framework for automated trading with risk management features for the Hyper Liquid platform. Ensure thorough testing and customization based on your trading strategy and risk tolerance.