from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import SessionLocal

router = APIRouter(
    prefix="/checkout",
    tags=["checkout"],
    responses={404: {"description": "Not found"}},
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_whatsapp_link(whatsapp_number: str, message: str) -> str:
    """
    Generate a WhatsApp link with the given phone number and message.
    WhatsApp format: https://wa.me/{phone_number}?text={url_encoded_message}
    """
    import urllib.parse
    # Remove any non-digit characters from the phone number
    cleaned_number = ''.join(filter(str.isdigit, whatsapp_number))
    # URL encode the message
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{cleaned_number}?text={encoded_message}"

@router.get("/{user_identifier}", response_model=schemas.Product)
def get_checkout_link(user_identifier: str, db: Session = Depends(get_db)):
    """
    Generate a WhatsApp checkout link for the user's cart.
    Returns the link and cart details.
    """
    # Get the user's cart
    db_cart = crud.get_cart_by_user_identifier(db, user_identifier=user_identifier)
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Get cart with items
    cart_with_items = crud.get_cart_with_items(db, cart_id=db_cart.id)
    if not cart_with_items.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Build the message for WhatsApp
    message_lines = ["Hello, I'd like to place an order:"]
    total_amount = 0.0
    
    for item in cart_with_items.items:
        product = crud.get_product(db, product_id=item.product_id)
        if product:
            seller = crud.get_seller(db, seller_id=product.seller_id)
            item_total = product.price * item.quantity
            total_amount += item_total
            message_lines.append(
                f"- {product.name} (x{item.quantity}) @ ${product.price:.2f} each = ${item_total:.2f}"
            )
            if seller:
                message_lines.append(f"  From: {seller.name} (WhatsApp: {seller.whatsapp_number})")
    
    message_lines.append(f"\nTotal: ${total_amount:.2f}")
    message_lines.append("\nPlease confirm this order.")
    
    message = "\n".join(message_lines)
    
    # For simplicity, we'll use the first seller's WhatsApp number
    # In a real application, you might want to handle multiple sellers differently
    first_item = cart_with_items.items[0]
    first_product = crud.get_product(db, product_id=first_item.product_id)
    first_seller = crud.get_seller(db, seller_id=first_product.seller_id) if first_product else None
    
    if not first_seller or not first_seller.whatsapp_number:
        raise HTTPException(status_code=400, detail="Unable to generate WhatsApp link")
    
    whatsapp_link = generate_whatsapp_link(first_seller.whatsapp_number, message)
    
    return {
        "cart_id": db_cart.id,
        "user_identifier": user_identifier,
        "whatsapp_link": whatsapp_link,
        "message": message,
        "total_amount": total_amount,
        "items_count": len(cart_with_items.items)
    }