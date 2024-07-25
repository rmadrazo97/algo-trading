# Recent Trades Tracker

This Python script tracks recent trades for a list of specified cryptocurrency symbols from the Binance exchange and logs the trade details to a CSV file. Additionally, it prints significant trades to the console with color-coded output based on trade size and type.

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
   python recent_trades.py
   ```

## Script Overview

- **Symbols:** The script tracks trades for the following symbols: BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT, DOGE/USDT, and WI/USDT.
- **WebSocket URL:** The script connects to Binance's WebSocket API using the URL `wss://fstream.binance.com/ws/`.
- **CSV File:** Trades are logged to `binance_trades.csv`. If the file does not exist, it is created with the appropriate header.
- **Trade Stream:** The script opens a WebSocket connection for each symbol and listens for aggregate trade messages.
- **Trade Filtering and Display:** Significant trades (greater than $14,999) are printed to the console with different colors based on the trade type (BUY/SELL) and trade size.
- **Error Handling:** In case of an error, the script will sleep for 5 seconds before retrying the connection.

### Detailed Functionality

1. **CSV File Initialization:**
   - The script checks if `binance_trades.csv` exists. If not, it creates the file and writes the header.

2. **Binance Trade Stream:**
   - Connects to the WebSocket API for each symbol.
   - Receives trade messages in JSON format and extracts relevant trade details.
   - Converts the trade time to a readable format in the US/Eastern timezone.
   - Filters trades based on their USD size and prints significant trades to the console with color coding.
   - Logs all trades to the CSV file.

3. **Main Function:**
   - Creates a task for each symbol's trade stream.
   - Uses `asyncio.gather` to run all tasks concurrently.

### Example Output

Significant trades are printed to the console with the following format:
```
* BUY BTC 12:34:56 $50,000 
```
Where:
- `*` indicates the significance level based on the trade size.
- `BUY`/`SELL` indicates the trade type.
- `BTC` is the symbol.
- `12:34:56` is the trade time.
- `$50,000` is the trade size in USD.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Binance API](https://github.com/binance/binance-spot-api-docs) for providing the WebSocket stream.
- [Termcolor](https://pypi.org/project/termcolor/) for colorizing the console output.