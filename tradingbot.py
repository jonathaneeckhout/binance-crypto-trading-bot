import logging
import argparse
import configparser
from trader.connector import Connector
from trader.wallet import Wallet
from trader.strategies.gridstrategy import GridStrategy
from trader.strategies.intervalstrategy import IntervalStrategy


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments namespace containing the config file path, API key, and API secret.
    """
    parser = argparse.ArgumentParser(
        description="Start the trading bot with the specified configuration."
    )

    parser.add_argument("config", help="Path to the config file to be used", type=str)
    parser.add_argument("-k", "--key", help="Binance API key")
    parser.add_argument("-s", "--secret", help="Binance API secret")
    args = parser.parse_args()

    return args


def configure_logger(log_to_file: bool, log_file: str, log_level: int) -> None:
    """
    Configures the logging settings.

    Args:
        log_to_file (bool): If True, logs will be written to a file. Otherwise, logs will be written to the console.
        log_file (str): The file path to write logs if log_to_file is True.
        log_level (int): The logging level (e.g., logging.DEBUG, logging.INFO).
    """
    format = "%(asctime)s %(levelname)-s [%(filename)s:%(lineno)d] %(message)s"

    if log_to_file:
        logging.basicConfig(
            filename=log_file,
            format=format,
            filemode="w",
        )
    else:
        logging.basicConfig(
            format=format,
            handlers=[logging.StreamHandler()],  # Output logs to the console
        )

    # Creating an object
    logger = logging.getLogger()

    # Setting the threshold of logger to the specified log level
    logger.setLevel(log_level)


def main() -> None:
    """
    Main function to start the trading bot.

    It parses the command-line arguments, reads the configuration file, sets up logging,
    and initializes and starts the Connector class.
    """
    args = parse_arguments()

    # Read out the config file
    config = configparser.ConfigParser()
    config.read(args.config)

    # Get the value for log level from the config file
    log_level = getattr(logging, config.get("logging", "level").upper(), None)
    if not isinstance(log_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    # Configure the logger
    configure_logger(
        config.getboolean("logging", "log_to_file"),
        config.get("logging", "file"),
        log_level,
    )

    # Initialize the connector class
    connector = Connector(
        stream_url=config.get("binance", "stream_url"),
        symbol=config.get("binance", "symbol"),
    )

    wallet = Wallet(
        api_url=config.get("binance", "api_url"),
        api_key=args.key,
        api_secret=args.secret,
    )

    if config.getboolean("grid_strategy", "enable"):
        # Initialize the grid strategy
        grid_strategy = GridStrategy(
            symbol=config.get("binance", "symbol"),
            grid_reference_price=config.getfloat("grid_strategy", "reference_price"),
            grid_size=config.getint("grid_strategy", "size"),
            grid_spacing=config.getfloat("grid_strategy", "spacing"),
            grid_amount_per_trade=config.getfloat("grid_strategy", "amount_per_trade"),
            wallet=wallet,
        )

        # Register the tick callback
        connector.register_tick_callback(grid_strategy.tick_callback)

    if config.getboolean("interval_strategy", "enable"):
        # Initialize the interval strategy
        interval_strategy = IntervalStrategy(
            symbol=config.get("binance", "symbol"),
            interval_time=config.getint("interval_strategy", "interval_time"),
            amount_per_trade=config.getfloat("interval_strategy", "amount_per_trade"),
            wallet=wallet,
        )

        # Register the tick callback
        connector.register_tick_callback(interval_strategy.tick_callback)

    # Start the connector
    connector.start()


if __name__ == "__main__":
    main()
