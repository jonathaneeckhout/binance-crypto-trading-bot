# binance-crypto-trading-bot
This app connects to the Binance 24-hour ticker, maintaining a stable connection to receive real-time market data. The trading logic processes these values to trigger buy or sell signals based on predefined criteria.

Key Features:

  * Stable Connection: Seamlessly connects to Binance's 24h ticker.
  * Real-time Trading Logic: Evaluates market data to generate buy or sell signals.
  * Configurable Settings: Easily customize trading parameters.
  * Comprehensive Logging: Detailed logs for all operations and signals.
  * Flexible Deployment: Easily deployable as a Docker image or run in a Python virtual environment.

# usage

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
