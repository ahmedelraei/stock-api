from datetime import datetime
from typing_extensions import Self


class Stock:
    """Stock Model"""

    stocks = {}

    def __init__(
        self, stock_id: int, name: str, price: float, availability: int, timestamp: datetime
    ) -> None:
        self.id = stock_id
        self.price = price
        self.availability = availability
        self.timestamp = timestamp
        self.day_peak = {
            "timestamp": timestamp,
            "price": price,
        }
        self.day_bottom = {
            "timestamp": timestamp,
            "price": price,
        }
        self.hour_peak = {
            "timestamp": timestamp,
            "price": price,
        }
        self.hour_bottom = {
            "timestamp": timestamp,
            "price": price,
        }
        self.change = 0
        self.stocks[stock_id] = self

    def __iter__(self):
        yield "id", self.id
        yield "price", self.price
        yield "change", self.change
        yield "availability", self.availability
        yield "day_peak", self.day_peak["price"]
        yield "day_bottom", self.day_bottom["price"]
        yield "hour_peak", self.hour_peak["price"]
        yield "hour_bottom", self.hour_bottom["price"]
        yield "timestamp", self.timestamp

    @classmethod
    def process_prices(cls, stock: Self):
        # if stock.hour_peak["timestamp"].hour == datetime.utcnow().hour:
        if (
            stock.timestamp.hour > stock.hour_peak["timestamp"].hour
            or max(stock.price, stock.hour_peak["price"]) == stock.price
        ):
            stock.hour_peak["price"] = stock.price
            stock.hour_peak["timestamp"] = stock.timestamp
        elif (
            stock.timestamp.hour > stock.hour_peak["timestamp"].hour
            or min(stock.price, stock.hour_bottom["price"]) == stock.price
        ):
            stock.hour_bottom["price"] = stock.price
            stock.hour_bottom["timestamp"] = stock.timestamp

        if (
            stock.timestamp.date() > stock.day_peak["timestamp"].date()
            or max(stock.price, stock.day_peak["price"]) == stock.price
        ):
            stock.day_peak["price"] = stock.price
            stock.day_peak["timestamp"] = stock.timestamp
        elif (
            stock.timestamp.date() > stock.day_peak["timestamp"].date()
            or min(stock.price, stock.day_bottom["price"]) == stock.price
        ):
            stock.day_bottom["price"] = stock.price
            stock.day_bottom["timestamp"] = stock.timestamp

    @classmethod
    def get(cls, stock_id) -> Self:
        return cls.stocks.get(stock_id, None)

    @classmethod
    def all(cls) -> list:
        return list(cls.stocks.values())

    @classmethod
    def create_or_update(
        cls, stock_id: int, name: str, price: float, availability: int, timestamp: str
    ) -> Self:
        timestamp: datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        stock = cls.get(stock_id)
        if stock:
            try:
                stock.change = round(((price - stock.price) / stock.price) * 100, 2)
            except ZeroDivisionError:
                stock.change = round(((price - stock.price) / 1) * 100, 2)
            stock.name = name
            stock.price = price
            stock.availability = availability
            stock.timestamp = timestamp
            cls.process_prices(stock)
            return stock
        return cls(
            stock_id,
            name,
            price,
            availability,
            timestamp,
        )
