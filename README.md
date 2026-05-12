# E-commerce API

A backend API for an e-commerce site that leads clients to sellers' WhatsApp with cart functionality, built with FastAPI.

## Features

- Product management (CRUD operations)
- Seller management with WhatsApp integration
- Cart functionality (add/update/remove items)
- WhatsApp checkout link generation
- SQLite database for persistence

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Initialize the database:

   ```bash
   python create_db.py
   ```

3. Run the API:

   ```bash
   uvicorn main:app --reload
   ```

4. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Products

- `POST /products/` - Create a new product
- `GET /products/` - Get all products
- `GET /products/{product_id}` - Get a specific product

### Cart

- `POST /cart/` - Create or get a cart for a user
- `GET /cart/{user_identifier}` - Get a user's cart with items
- `POST /cart/{user_identifier}/items` - Add an item to cart
- `PUT /cart/items/{cart_item_id}` - Update cart item quantity
- `DELETE /cart/items/{cart_item_id}` - Remove item from cart

### Checkout

- `GET /checkout/{user_identifier}` - Generate WhatsApp checkout link for user's cart

## Data Models

- **Seller**: id, name, whatsapp_number, created_at
- **Product**: id, name, description, price, seller_id, created_at
- **Cart**: id, user_identifier, created_at
- **CartItem**: id, cart_id, product_id, quantity, added_at

## Testing

Run the test script to see example usage:

```bash
python test_api.py
```

(Make sure the API is running first)

## Notes

- This API uses SQLite for simplicity. For production, consider using PostgreSQL or MySQL.
- Authentication is not implemented in this version. In a real application, you would want to add user authentication.
- The WhatsApp link generation uses the first seller's number from the cart items. For carts with multiple sellers, you might want to implement a different strategy.
