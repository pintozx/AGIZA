from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SellerBase(BaseModel):
    name: str
    whatsapp_number: str

class SellerCreate(SellerBase):
    pass

class Seller(SellerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    seller_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CartBase(BaseModel):
    user_identifier: str

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    cart_id: int
    added_at: datetime

    class Config:
        orm_mode = True

class CartWithItems(Cart):
    items: list[CartItem] = []

    class Config:
        orm_mode = True