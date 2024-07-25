# Funding Rate Tracker

This Python script tracks the funding rates for a list of specified cryptocurrency symbols from the Binance exchange. It displays the yearly funding rates with color-coded output based on the rate magnitude.

## Requirements

- Python 3.8+
- Conda (optional, for managing dependencies)

## Dependencies

The script requires the following Python packages:

- `asyncio`
- `json`
- `datetime`
- `websockets`
- `termcolor`

You can install these dependencies using Conda and pip:

```bash
conda create --name trades_env python=3.8
conda activate trades_env
conda install -c conda-forge asyncio termcolor websockets
pip install websockets termcolor
```

## Usage

1. **Activate the Conda environment:**
   ```bash
   conda activate trades_env
   ```

2. **Run the script:**
   ```bash
   python funding.py
   ```

## Script Overview

- **Symbols:** The script tracks funding rates for the following symbols: BTC/USDT, ETH/USDT, SOL/USDT, and WI/USDT.
- **WebSocket URL:** The script connects to Binance's WebSocket API using the URL `wss://fstream.binance.com/ws/`.
- **Funding Rate Display:** The script calculates the yearly funding rate from the received funding rate and displays it with color-coded output based on the rate magnitude.
- **Shared Symbol Counter:** A shared counter is used to display a summary message after processing the funding rate for all symbols.

### Detailed Functionality

1. **WebSocket Connection:**
   - Connects to the WebSocket API for each symbol's mark price stream.
   - Receives funding rate messages in JSON format and extracts relevant details.

2. **Yearly Funding Rate Calculation:**
   - Converts the funding rate to a yearly rate by multiplying it by 3 (for 8-hour periods in a day) and by 365 (for days in a year), and then by 100 to get a percentage.

3. **Color-Coded Output:**
   - Displays the yearly funding rate with different background colors based on its value:
     - Red: > 50%
     - Yellow: > 30%
     - Cyan: > 5%
     - Green: < -10%
     - Light Green: Otherwise

4. **Shared Symbol Counter:**
   - Keeps track of the number of processed symbols.
   - Displays a summary message after processing all symbols.

5. **Error Handling:**
   - In case of an error, the script will sleep for 5 seconds before retrying the connection.

### Example Output

Funding rates are printed to the console with the following format:
```
BTC funding: 60.00%
ETH funding: 35.00%
SOL funding: 10.00%
WI funding: -15.00%
```
With different background colors based on the funding rate value.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Binance API](https://github.com/binance/binance-spot-api-docs) for providing the WebSocket stream.
- [Termcolor](https://pypi.org/project/termcolor/) for colorizing the console output.