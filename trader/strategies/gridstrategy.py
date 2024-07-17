from trader.wallet import Wallet


class Order:
    def __init__(self, name: str, buy_price: float, sell_price: float) -> None:
        self.running = False  # Indicates if the order is currently active
        self.name = name  # Name/ID of the order
        self.buy_price = buy_price  # Price to buy at
        self.sell_price = sell_price  # Price to sell at
        self.crypto_holdings = 0.0  # Amount of cryptocurrency held


class GridStrategy:
    def __init__(
        self,
        symbol: str,
        grid_reference_price: float,
        grid_size: int,
        grid_spacing: float,
        grid_amount_per_trade: float,
        wallet: Wallet,
    ) -> None:
        self.__symbol = symbol  # Trading symbol

        self.__grid_reference_price = grid_reference_price  # Reference price for grid
        self.__grid_size = grid_size  # Number of grid levels
        self.__grid_spacing = grid_spacing  # Price spacing between grid levels
        self.__grid_amount_per_trade = grid_amount_per_trade  # Amount per trade
        self.__wallet = wallet  # Wallet object

        self.__orders = []  # List of grid orders

        self._create_grid_orders()

    def tick_callback(self, data: object):
        # Extract time and price from the data
        try:
            price = float(data["c"])
        except KeyError:
            return

        for order in self.__orders:
            # Process each order with the current time and price
            self._process_order(order, price)

    def _create_grid_orders(self):
        # Create grid orders based on reference price, size, and spacing
        self.__orders = []
        for i in range(1, self.__grid_size + 1):
            self.__orders.append(
                Order(
                    f"grid_{i}",
                    self.__grid_reference_price - i * self.__grid_spacing,
                    self.__grid_reference_price - (i - 1) * self.__grid_spacing,
                )
            )

    def _process_order(self, order: Order, price: float) -> None:
        # Handle buy and sell logic for an order
        if not order.running and price <= order.buy_price:
            self.__wallet.place_market_buy_order(
                self.__symbol, self.__grid_amount_per_trade
            )
            order.running = True

        elif order.running and price >= order.sell_price:
            self.__wallet.place_market_sell_order(self.__symbol, order.crypto_holdings)
            order.running = False
