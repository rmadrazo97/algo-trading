# Huge Trades Tracker

This Python script aggregates and tracks large trades for a list of specified cryptocurrency symbols from the Binance exchange. It logs the trade details to a CSV file and prints significant aggregated trades to the console.

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
   python huge_trades.py
   ```

## Script Overview

- **Symbols:** The script tracks trades for the following symbols: BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT, DOGE/USDT, and WI/USDT.
- **WebSocket URL:** The script connects to Binance's WebSocket API using the URL `wss://fstream.binance.com/ws/`.
- **CSV File:** Trades are logged to `binance_trades.csv`. If the file does not exist, it is created with the appropriate header.
- **Trade Aggregation:** The script aggregates trades per second and checks if the total trade size exceeds a threshold.
- **Significant Trade Display:** Aggregated trades with a USD size greater than $500,000 are printed to the console with color-coded output.
- **Error Handling:** In case of an error, the script will sleep for 5 seconds before retrying the connection.

### Detailed Functionality

1. **CSV File Initialization:**
   - The script checks if `binance_trades.csv` exists. If not, it creates the file and writes the header.

2. **Trade Aggregator Class:**
   - `TradeAggregator` class maintains a dictionary to bucket trades by symbol, second, and whether the trade is a buyer maker.
   - `add_trade` method adds trades to the appropriate bucket.
   - `check_and_print_trades` method checks for trades exceeding the $500,000 threshold and prints them.

3. **Binance Trade Stream:**
   - Connects to the WebSocket API for each symbol.
   - Receives trade messages in JSON format and extracts relevant trade details.
   - Adds trades to the aggregator for further processing.

4. **Main Function:**
   - Creates a task for each symbol's trade stream.
   - Creates a task to print aggregated trades every second.
   - Uses `asyncio.gather` to run all tasks concurrently.

### Example Output

Significant trades are printed to the console with the following format:
```
BUY BTC 12:34:56 $0.50m
```
Where:
- `BUY`/`SELL` indicates the trade type.
- `BTC` is the symbol.
- `12:34:56` is the trade time.
- `$0.50m` is the trade size in millions of USD.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Binance API](https://github.com/binance/binance-spot-api-docs) for providing the WebSocket stream.
- [Termcolor](https://pypi.org/project/termcolor/) for colorizing the console output.
