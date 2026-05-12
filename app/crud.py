from sqlalchemy.orm import Session
from . import models, schemas

def get_seller(db: Session, seller_id: int):
    return db.query(models.Seller).filter(models.Seller.id == seller_id).first()

def get_sellers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Seller).offset(skip).limit(limit).all()

def create_seller(db: Session, seller: schemas.SellerCreate):
    db_seller = models.Seller(**seller.dict())
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_cart(db: Session, cart_id: int):
    return db.query(models.Cart).filter(models.Cart.id == cart_id).first()

def get_cart_by_user_identifier(db: Session, user_identifier: str):
    return db.query(models.Cart).filter(models.Cart.user_identifier == user_identifier).first()

def create_cart(db: Session, cart: schemas.CartCreate):
    db_cart = models.Cart(**cart.dict())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def get_cart_item(db: Session, cart_item_id: int):
    return db.query(models.CartItem).filter(models.CartItem.id == cart_item_id).first()

def get_cart_items_by_cart(db: Session, cart_id: int):
    return db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id).all()

def create_cart_item(db: Session, cart_item: schemas.CartItemCreate, cart_id: int):
    db_cart_item = models.CartItem(**cart_item.dict(), cart_id=cart_id)
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def update_cart_item_quantity(db: Session, cart_item_id: int, quantity: int):
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id).first()
    if db_cart_item:
        db_cart_item.quantity = quantity
        db.commit()
        db.refresh(db_cart_item)
    return db_cart_item

def delete_cart_item(db: Session, cart_item_id: int):
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id).first()
    if db_cart_item:
        db.delete(db_cart_item)
        db.commit()
    return db_cart_item

def get_cart_with_items(db: Session, cart_id: int):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if cart:
        items = db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id).all()
        cart.items = items
    return cart