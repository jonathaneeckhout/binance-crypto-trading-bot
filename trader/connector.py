import logging
import json
import time

from binance.websocket.spot.websocket_stream import (
    SpotWebsocketStreamClient,
)


class Connector:
    retry_time = 10.0

    def __init__(self, stream_url: str, symbol: str) -> None:
        self.__stream_url = stream_url
        self.__symbol = symbol

    @staticmethod
    def translate_ticker_data(data: dict) -> dict:
        # Mapping Binance's ticker data keys to more readable keys
        mapping = {
            "e": "Event Type",
            "E": "Event Time",
            "s": "Symbol",
            "p": "Price Change",
            "P": "Price Change Percent",
            "w": "Weighted Average Price",
            "x": "Previous Close Price",
            "c": "Current Close Price",
            "Q": "Last Trade Quantity",
            "b": "Best Bid Price",
            "B": "Best Bid Quantity",
            "a": "Best Ask Price",
            "A": "Best Ask Quantity",
            "o": "Open Price",
            "h": "High Price",
            "l": "Low Price",
            "v": "Base Asset Volume",
            "q": "Quote Asset Volume",
            "O": "Open Time",
            "C": "Close Time",
            "F": "First Trade ID",
            "L": "Last Trade ID",
            "n": "Number of Trades",
        }

        # Translate the ticker data using the mapping
        return {mapping.get(key, key): value for key, value in data.items()}

    def start(self) -> None:
        logging.info("Starting broker connector")

        # Initialize the Binance WebSocket Stream Client with the given URL and message handler
        self.stream_client = SpotWebsocketStreamClient(
            stream_url=self.__stream_url,
            on_message=self._message_handler,
            on_close=self._close_handler,
            on_error=self._error_handler,
        )

        self.stream_client.ticker(symbol=self.__symbol)

    def _message_handler(self, _, message: str) -> None:
        try:
            # Attempt to parse the incoming message as JSON
            json_message = json.loads(message)
            logging.debug("Binance input message={}".format(json_message))
        except ValueError:
            # Log a warning if the message could not be parsed
            logging.warn("Could not parse json result of server")
            return

        try:
            # Handle different event types from the JSON message
            match json_message["e"]:
                case "24hrTicker":
                    # TODO: handle the message
                    pass
                case _:
                    logging.info("Unknown event type")
        except KeyError:
            # If the event type key is missing, return silently
            return

    def _close_handler(self) -> None:
        self._retry_connection()

    def _error_handler(self, _, error) -> None:
        self._retry_connection()

    def _retry_connection(self) -> None:
        logging.info(
            f"Error occurred closed, retrying to connect in {Connector.retry_time} seconds"
        )

        time.sleep(Connector.retry_time)

        self.start()
