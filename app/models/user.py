from typing_extensions import Self
from .stock import Stock
from pydantic import BaseModel


class UserBaseModel(BaseModel):
    id: int
    username: str
    balance: float
    assets: dict[str, int]


class User:
    """User Model"""

    users = {}
    count = 0

    def __init__(self, username: str) -> None:
        self.id = self.count + 1
        self.username = username
        self.balance = 0
        self.__shares = {}
        type(self).users[self.id] = self
        type(self).count += 1

    def __iter__(self):
        yield "id", self.id
        yield "username", self.username
        yield "balance", self.balance
        yield "assets", self.assets()

    @classmethod
    def get_user(cls, id: int) -> Self:
        return cls.users.get(id, None)

    def set_shares(self, stock_id: str, shares: int) -> None:
        if shares == 0:
            del self.__shares[stock_id]
            return
        self.__shares[stock_id] = shares

    def get_shares(self, stock_id: str) -> dict:
        return self.__shares.get(stock_id, 0)

    def assets(self):
        return self.__shares
