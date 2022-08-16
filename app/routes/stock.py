from datetime import datetime, timezone
import threading
import time
from typing import Union
from fastapi import APIRouter, HTTPException
from ..models.user import User
from ..models.stock import Stock
from ..models.order import Order, OrderAction, OrderType, OrderBehaviour, OrderCreateModel

router = APIRouter()


@router.get("/stock/")
async def list_stocks():
    return Stock.all()


@router.get("/stock/{stock_id}")
async def stock(stock_id: str):
    stock = Stock.get(stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return Stock.get(stock_id)


class ProcessOrderThread(threading.Thread):
    def __init__(
        self,
        timeout,
        user: User,
        stock: Stock,
        limit: Union[list[float, float], None],
        order: Order,
    ):
        threading.Thread.__init__(self)
        self.timeout = timeout
        self.user = user
        self.stock = stock
        self.limit = limit
        self.order = order

    def run(self):
        qty = (
            self.order.total
            if self.stock.availability >= self.order.total
            else self.stock.availability
        )
        while True:
            if time.time() > self.timeout:
                self.order.cancelled = True
                break
            if self.limit:
                if not self.limit[0] <= self.stock.price <= self.limit[1]:
                    continue
            if (
                self.order.all_or_none or self.order.order_behaviour == OrderBehaviour.FOK
            ) and qty != self.order.total:
                self.order.cancelled = True
                break

            total_amount = self.stock.price * qty

            # Buy
            if self.order.action == OrderAction.BUY:
                if total_amount > self.user.balance:
                    self.order.cancelled = True
                    break
                self.user.balance -= total_amount
                self.user.set_shares(
                    self.stock.id, self.user.get_shares(self.stock.id) + qty
                )
            # Sell
            else:
                if self.order.total > self.user.get_shares(self.stock.id):
                    self.order.cancelled = True
                    break
                self.user.balance += total_amount
                self.user.set_shares(
                    self.stock.id, self.user.get_shares(self.stock.id) - self.order.total
                )
            self.order.price = self.stock.price
            self.order.succeed = True
            break


async def process_order(action: OrderAction, order: OrderCreateModel):
    user = User.get_user(order.user_id)
    stock = Stock.get(order.stock_id)
    if not user:
        raise HTTPException(404, "User not found!")
    if not stock:
        raise HTTPException(404, "Stock not found!")

    price_assumption = stock.price  # Initial Price Assumption With The Market Value

    limit = None
    if order.order_type == OrderType.LIMIT:
        price_assumption = order.upper_bound * order.total
        if not order.lower_bound:
            raise HTTPException(422, "You must specify lower bound")
        if not order.upper_bound:
            raise HTTPException(422, "You must specify upper bound")
        if order.lower_bound > order.upper_bound:
            raise HTTPException(403, detail="Upper bound must be greater than lower bound")

        limit = [order.lower_bound, order.upper_bound]

    if action == OrderAction.BUY and price_assumption > user.balance:
        raise HTTPException(403, "Insufficient funds")

    elif action == OrderAction.SELL and order.total > user.get_shares(stock.id):
        raise HTTPException(403, "You don't own assets of this stock")

    # Initialize An Order Instance
    order_obj = Order(
        user_id=user.id,
        stock_id=order.stock_id,
        total=order.total,
        order_type=order.order_type,
        order_behaviour=order.order_behaviour,
        action=action,
        price=price_assumption,
        all_or_none=order.all_or_none,
    )

    timeout = time.time()

    # assmuption price: market price or upper bound (ONLY INITIAL ASSUMPTION) in case of limit order type.

    # Behaviour 1 (DAY): User chose to wait until the
    # stock price fall within [assumption price] for 24 hours
    if order.order_behaviour == OrderBehaviour.DAY:
        timeout += 60 * 60 * 24

    # Behaviour 2 (GTC): User chose to wait for the catching process
    # of price falling until he cancel it himself
    elif order.order_behaviour == OrderBehaviour.GTC:
        EPOCH_MAX = 2**63 / 1e9 - 0.1
        timeout = EPOCH_MAX

    # Behaviour 3 (IOC): User chose to buy shares within the [assumption price]
    # immediately even if only some of desired # of shares falled within
    # [assumption price]. if no share falls order cancels.
    elif order.order_behaviour == OrderBehaviour.IOC:
        timeout += 60

    # Behaviour 4 (FOK): User chose to buy shares within the [assumption price] only
    # or order got cancelled
    elif order.order_behaviour == OrderBehaviour.FOK:
        timeout += 60

    # Behaviour 5 (GTD): User chose to buy shares within the [assumption price]
    # until desired date if price didn't fall orders cancels on date.
    elif order.order_behaviour == OrderBehaviour.GTD:
        if not order.date:
            raise HTTPException(422, "You must specify date.")
        delta_time = order.date - datetime.now(timezone.utc)
        timeout += delta_time.seconds

    # Starting a new thread to process purchase under specified conditions
    t = ProcessOrderThread(timeout, user, stock, limit, order_obj)
    t.start()

    return {"success": "Order has been just processed"}


@router.post("/buy")
async def buy(order: OrderCreateModel):
    return await process_order(OrderAction.BUY, order)


@router.post("/sell")
async def sell(order: OrderCreateModel):
    return await process_order(OrderAction.SELL, order)
