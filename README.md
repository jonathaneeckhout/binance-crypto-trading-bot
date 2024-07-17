# binance-crypto-trading-bot
An automatic trading bot for binance


# usage

## Using virtual environment
Create a venv
```bash
./scripts/create_venv.sh
```

Start your venv session
```bash
source ./scripts/start_venv.sh
```

Run bot
```bash
python3 tradingbot.py -k <YOUR BINANCE API KEY> -s <YOUR BINANCE API SECRET> config.ini
```