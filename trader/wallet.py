import logging

from binance.spot import Spot
from binance.error import ClientError


class Wallet:
    def __init__(self, api_url: str, api_key: str, api_secret: str):
        self.client = Spot(api_key=api_key, api_secret=api_secret, base_url=api_url)

    def place_market_buy_order(self, symbol: str, quantity: float):
        params = {
            "symbol": symbol,
            "side": "BUY",
            "type": "MARKET",
            "quantity": quantity,
        }

        try:
            response = self.binance_client.new_order(**params)
            logging.info(response)
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    def place_market_sell_order(self, symbol: str, quantity: float):
        params = {
            "symbol": symbol,
            "side": "SELL",
            "type": "MARKET",
            "quantity": quantity,
        }

        try:
            response = self.binance_client.new_order(**params)
            logging.info(response)
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
