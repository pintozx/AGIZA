from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import SessionLocal

router = APIRouter(
    prefix="/cart",
    tags=["cart"],
    responses={404: {"description": "Not found"}},
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Cart, status_code=status.HTTP_201_CREATED)
def create_cart(cart: schemas.CartCreate, db: Session = Depends(get_db)):
    # Check if cart already exists for this user
    db_cart = crud.get_cart_by_user_identifier(db, user_identifier=cart.user_identifier)
    if db_cart:
        return db_cart
    return crud.create_cart(db=db, cart=cart)

@router.get("/{user_identifier}", response_model=schemas.CartWithItems)
def read_cart(user_identifier: str, db: Session = Depends(get_db)):
    db_cart = crud.get_cart_by_user_identifier(db, user_identifier=user_identifier)
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_with_items = crud.get_cart_with_items(db, cart_id=db_cart.id)
    return cart_with_items

@router.post("/{user_identifier}/items", response_model=schemas.CartItem, status_code=status.HTTP_201_CREATED)
def add_item_to_cart(user_identifier: str, cart_item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    # Get or create cart for user
    db_cart = crud.get_cart_by_user_identifier(db, user_identifier=user_identifier)
    if not db_cart:
        cart_create = schemas.CartCreate(user_identifier=user_identifier)
        db_cart = crud.create_cart(db=db, cart=cart_create)
    
    # Check if product exists
    product = crud.get_product(db, product_id=cart_item.product_id)
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")
    
    # Check if item already in cart
    existing_items = crud.get_cart_items_by_cart(db, cart_id=db_cart.id)
    for item in existing_items:
        if item.product_id == cart_item.product_id:
            # Update quantity instead of adding new item
            updated_item = crud.update_cart_item_quantity(
                db, 
                cart_item_id=item.id, 
                quantity=item.quantity + cart_item.quantity
            )
            return updated_item
    
    # Create new cart item
    return crud.create_cart_item(db=db, cart_item=cart_item, cart_id=db_cart.id)

@router.put("/items/{cart_item_id}", response_model=schemas.CartItem)
def update_cart_item(cart_item_id: int, cart_item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    db_cart_item = crud.get_cart_item(db, cart_item_id=cart_item_id)
    if db_cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Check if product exists
    product = crud.get_product(db, product_id=cart_item.product_id)
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")
    
    updated_item = crud.update_cart_item_quantity(
        db, 
        cart_item_id=cart_item_id, 
        quantity=cart_item.quantity
    )
    return updated_item

@router.delete("/items/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cart_item(cart_item_id: int, db: Session = Depends(get_db)):
    db_cart_item = crud.get_cart_item(db, cart_item_id=cart_item_id)
    if db_cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    crud.delete_cart_item(db=db, cart_item_id=cart_item_id)
    return {"ok": True}