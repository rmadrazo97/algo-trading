# Binance Big Liquidations Tracker

This Python script tracks large liquidation orders for all symbols on the Binance exchange. It logs the details of each significant liquidation order to a CSV file and displays them to the console with color-coded output.

## Requirements

- Python 3.8+
- Conda (optional, for managing dependencies)

## Dependencies

The script requires the following Python packages:

- `asyncio`
- `json`
- `os`
- `datetime`
- `pytz`
- `websockets`
- `termcolor`

You can install these dependencies using Conda and pip:

```bash
conda create --name trades_env python=3.8
conda activate trades_env
conda install -c conda-forge asyncio pytz termcolor websockets
pip install websockets termcolor
```

## Usage

1. **Activate the Conda environment:**
   ```bash
   conda activate trades_env
   ```

2. **Run the script:**
   ```bash
   python big_liqs.py
   ```

## Script Overview

- **WebSocket URL:** The script connects to Binance's WebSocket API using the URL `wss://fstream.binance.com/ws/!forceOrder@arr` to receive liquidation order data.
- **CSV File:** Liquidation orders are logged to `binance_bigliqs.csv`. If the file does not exist, it is created with the appropriate header.
- **Liquidation Display:** The script prints significant liquidations (those greater than $100,000) to the console with color-coded output based on the liquidation size.

### Detailed Functionality

1. **CSV File Initialization:**
   - The script checks if `binance_bigliqs.csv` exists. If not, it creates the file and writes the header.

2. **WebSocket Connection:**
   - Connects to the WebSocket API for liquidation orders.
   - Receives liquidation messages in JSON format and extracts relevant details.

3. **Liquidation Details:**
   - Calculates the USD size of each liquidation order.
   - Converts the order timestamp to a readable format in the US/Eastern timezone.

4. **Color-Coded Output:**
   - Displays significant liquidations with different background colors based on their size:
     - Liquidations > $100,000 are displayed.
     - Liquidations are color-coded as follows:
       - Blue background for SELL liquidations.
       - Magenta background for BUY liquidations.

5. **Error Handling:**
   - In case of an error, the script will sleep for 5 seconds before retrying the connection.

### Example Output

Liquidation orders are printed to the console with the following format:
```
L LIQ BTC 12:34:56 0.10
```
Where:
- `L LIQ` indicates a long liquidation (sell).
- `S LIQ` indicates a short liquidation (buy).
- `BTC` is the symbol.
- `12:34:56` is the liquidation time.
- `0.10` is the liquidation size in millions of USD.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Binance API](https://github.com/binance/binance-spot-api-docs) for providing the WebSocket stream.
- [Termcolor](https://pypi.org/project/termcolor/) for colorizing the console output.