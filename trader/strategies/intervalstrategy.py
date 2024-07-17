from trader.wallet import Wallet


class IntervalStrategy:
    def __init__(
        self, symbol: str, interval_time: int, amount_per_trade: float, wallet: Wallet
    ):
        self.__symbol = symbol  # Trading symbol
        self.__interval_time = interval_time  # Interval time in miliseconds
        self.__amount_per_trade = amount_per_trade  # Amount per tradei
        self.__last_trade_time = 0  # Last trade time in miliseconds
        self.__wallet = wallet  # Wallet object
        self.__crypto_holdings = 0.0  # Amount of cryptocurrency held

    def tick_callback(self, data: object):
        # Extract time and price from the data
        try:
            time = int(data["E"])
        except KeyError:
            return

        # Check if the interval has passed
        if time - self.__last_trade_time >= self.__interval_time:
            self.__last_trade_time = time

            if self.__crypto_holdings == 0:
                self.__crypto_holdings = self.__wallet.place_market_buy_order(
                    self.__symbol, self.__amount_per_trade
                )
            else:
                if (
                    self.__wallet.place_market_sell_order(
                        self.__symbol, self.__crypto_holdings
                    )
                    > 0.0
                ):
                    self.__crypto_holdings = 0.0
