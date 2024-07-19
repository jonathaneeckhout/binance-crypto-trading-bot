# binance-crypto-trading-bot
This app connects to the Binance 24-hour ticker, maintaining a stable connection to receive real-time market data. The trading logic processes these values to trigger buy or sell signals based on predefined criteria.

Key Features:

  * Stable Connection: Seamlessly connects to Binance's 24h ticker.
  * Real-time Trading Logic: Evaluates market data to generate buy or sell signals.
  * Configurable Settings: Easily customize trading parameters.
  * Comprehensive Logging: Detailed logs for all operations and signals.
  * Flexible Deployment: Easily deployable as a Docker image or run in a Python virtual environment.

Example of configuration
```
[interval_strategy]
; Interval trading strategy enable/disable
enable = True
; Amount of currency (e.g., BTC) per trade
amount_per_trade = 0.00015000
; Interval time in miliseconds
interval_time = 10000
```

Example logging
```bash
2024-07-19 10:36:28,588 INFO [tradingbot.py:97] GridStrategy is enabled
2024-07-19 10:36:28,588 INFO [tradingbot.py:115] IntervalStrategy is enabled
2024-07-19 10:36:28,588 INFO [connector.py:53] Starting broker connector
2024-07-19 10:36:34,588 INFO [intervalstrategy.py:29] Placing buy order
2024-07-19 10:36:34,588 INFO [wallet.py:12] Placing buy order for BTCEUR with 0.00015
2024-07-19 10:36:35,612 INFO [wallet.py:25] Order filled for 0.00015000 BTCEUR
2024-07-19 10:36:46,568 INFO [intervalstrategy.py:34] Placing sell order
2024-07-19 10:36:46,568 INFO [wallet.py:44] Placing sell order for 0.00015 BTCEUR
2024-07-19 10:36:47,286 INFO [wallet.py:59] Order filled for 0.00015000 BTCEUR
```

# Usage

## Using virtual environment
Create a venv
```bash
./scripts/create_venv.sh
```

Start your virtual environment session
```bash
source ./scripts/start_venv.sh
```

Run bot
```bash
python3 tradingbot.py -k <YOUR BINANCE API KEY> -s <YOUR BINANCE API SECRET> config.ini
```
