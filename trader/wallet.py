import logging

from binance.spot import Spot
from binance.error import ClientError


class Wallet:
    def __init__(self, api_url: str, api_key: str, api_secret: str):
        self.__client = Spot(api_key=api_key, api_secret=api_secret, base_url=api_url)

    def place_market_buy_order(self, symbol: str, quantity: float) -> float:
        logging.info(f"Placing buy order for {symbol} with {quantity} base currency ")

        params = {
            "symbol": symbol,
            "side": "BUY",
            "type": "MARKET",
            "quoteOrderQty": quantity,
        }

        try:
            response = self.__client.new_order(**params)
            logging.debug(response)
            if response["status"] == "FILLED":
                logging.info(
                    f"Order filled for {response['executedQty']} {symbol} traded currency"
                )

                return float(
                    response["executedQty"]
                )  # Convert to float before returning
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

        logging.warning("Order not filled")

        return 0.0

    def place_market_sell_order(self, symbol: str, quantity: float) -> float:
        logging.info(f"Placing sell order for traded currency {quantity} {symbol}")

        params = {
            "symbol": symbol,
            "side": "SELL",
            "type": "MARKET",
            "quantity": quantity,
        }

        try:
            response = self.__client.new_order(**params)
            logging.debug(response)

            if response["status"] == "FILLED":

                logging.info(
                    f"Order filled for {response['executedQty']} {symbol} base currency"
                )

                return float(
                    response["executedQty"]
                )  # Convert to float before returning
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

        logging.warning("Order not filled")

        return 0.0
