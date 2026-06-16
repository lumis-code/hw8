from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class FlowerBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    in_stock: int = Field(..., ge=0)


class FlowerCreate(FlowerBase):
    pass


class FlowerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    in_stock: Optional[int] = Field(None, ge=0)


class FlowerRead(FlowerBase):
    id: int

    class Config:
        from_attributes = True


class PurchaseStatusEnum(str, Enum):
    in_cart = "in_cart"
    purchased = "purchased"


class PurchaseCreate(BaseModel):
    flower_id: int
    quantity: int = Field(..., gt=0)
    status: Optional[PurchaseStatusEnum] = PurchaseStatusEnum.purchased


class PurchaseRead(BaseModel):
    id: int
    user_id: int
    flower_id: int
    quantity: int
    status: PurchaseStatusEnum
    created_at: datetime

    class Config:
        from_attributes = True


class CartItemRead(BaseModel):
    id: int
    flower_id: int
    quantity: int
    status: PurchaseStatusEnum
    created_at: datetime

    class Config:
        from_attributes = True
