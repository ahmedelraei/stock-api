from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..models.user import User, UserBaseModel

router = APIRouter()


@router.get("/user/{user_id}", response_model=UserBaseModel)
async def user(user_id: int):
    """Retrieve user by id"""
    user = User.get_user(user_id)
    if user is None:
        raise HTTPException(404, "User not found!")
    return user


class Operation(BaseModel):
    user_id: int
    amount: float = Field(gt=0)


@router.post("/deposit")
async def deposit(deposit: Operation):
    """deposits amount in user's account"""
    user = User.get_user(deposit.user_id)
    if user is None:
        raise HTTPException(404, "User not found!")
    user.balance += deposit.amount
    return {"success": f"You've successfully deposited {deposit.amount} EGP"}


@router.post("/withdraw")
async def withdraw(withdraw: Operation):
    """withdraws amount from user's account"""
    user = User.get_user(withdraw.user_id)
    if user is None:
        raise HTTPException(404, "User not found!")
    user.balance -= withdraw.amount
    return {"success": f"You've successfully withdrawn {withdraw.amount} EGP"}
