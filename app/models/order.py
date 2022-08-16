import enum
from typing import Optional
from typing_extensions import Self
from pydantic import BaseModel
from datetime import datetime


class OrderType(enum.Enum):
    LIMIT = "Limit"
    MARKET = "Market"


class OrderBehaviour(enum.Enum):
    DAY = "Day"
    GTC = "GTC"  # Good till cancel
    IOC = "IOC"  # Immediate or cancel ( All or some immediatley )
    FOK = "fill or kill"  # Fill or kill ( All )
    GTD = "GTD"  # Good to date


class OrderAction(enum.Enum):
    BUY = "Buy"
    SELL = "Sell"


class OrderBaseModel(BaseModel):
    id: int
    user_id: int
    stock_id: str
    price: float
    total: int
    net_total: float
    orderType: OrderType
    order_behaviour: OrderBehaviour
    all_or_none: bool
    succeed: bool
    cancelled: bool


class OrderCreateModel(BaseModel):
    user_id: int
    stock_id: str
    total: int
    order_type: OrderType
    order_behaviour: OrderBehaviour
    all_or_none: bool
    lower_bound: Optional[float]
    upper_bound: Optional[float]
    date: Optional[datetime]


class Order:
    count = 0
    orders = {}

    def __init__(
        self,
        user_id: int,
        stock_id: str,
        total: int,
        price: float,
        order_type: OrderType,
        order_behaviour: OrderBehaviour,
        action: OrderAction,
        all_or_none: bool = False,
    ) -> None:
        self.id = type(self).count + 1
        self.user_id = user_id
        self.stock_id = stock_id
        self.price = price
        self.total = total
        self.action = action
        self.orderType = order_type
        self.order_behaviour = order_behaviour
        self.all_or_none = all_or_none
        self.succeed = False
        self.cancelled = False
        type(self).orders[self.id] = self
        type(self).count += 1

    def __iter__(self):
        yield "id", self.id
        yield "user_id", self.user_id
        yield "stock_id", self.stock_id
        yield "price", self.price
        yield "total", self.total
        yield "net_total", self.net_total
        yield "orderType", self.orderType
        yield "order_behaviour", self.order_behaviour
        yield "all_or_none", self.all_or_none
        yield "succeed", self.succeed
        yield "cancelled", self.cancelled
    
    @property
    def net_total(self):
        return self.price * self.total

    @classmethod
    def orders_for_user(cls, user_id) -> list[Self]:
        for order in cls.orders.values():
            if order.user_id == user_id:
                yield order

    @classmethod
    def get(cls, id) -> Self:
        return cls.orders[id]
