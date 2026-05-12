"""
Simple test script to demonstrate API usage
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Test the root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print("Root endpoint:", response.json())

def test_create_seller():
    """Test creating a seller"""
    seller_data = {
        "name": "Test Seller",
        "whatsapp_number": "+1234567890"
    }
    response = requests.post(f"{BASE_URL}/products/", json=seller_data)
    print("Create seller:", response.json())
    return response.json()["id"] if response.status_code == 200 else None

def test_create_product(seller_id):
    """Test creating a product"""
    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": 29.99,
        "seller_id": seller_id
    }
    response = requests.post(f"{BASE_URL}/products/", json=product_data)
    print("Create product:", response.json())
    return response.json()["id"] if response.status_code == 200 else None

def test_get_products():
    """Test getting products"""
    response = requests.get(f"{BASE_URL}/products/")
    print("Get products:", response.json())

def test_cart_operations():
    """Test cart operations"""
    user_id = "test_user_123"
    
    # Create cart
    cart_data = {"user_identifier": user_id}
    response = requests.post(f"{BASE_URL}/cart/", json=cart_data)
    print("Create cart:", response.json())
    cart_id = response.json()["id"] if response.status_code == 200 else None
    
    # Add item to cart (assuming product_id 1 exists)
    if cart_id:
        cart_item_data = {
            "product_id": 1,
            "quantity": 2
        }
        response = requests.post(f"{BASE_URL}/cart/{user_id}/items", json=cart_item_data)
        print("Add item to cart:", response.json())
        
        # Get cart
        response = requests.get(f"{BASE_URL}/cart/{user_id}")
        print("Get cart:", response.json())
        
        # Get checkout link
        response = requests.get(f"{BASE_URL}/checkout/{user_id}")
        print("Get checkout link:", response.json())

if __name__ == "__main__":
    print("Testing E-commerce API...")
    print("Make sure the API is running on http://localhost:8000")
    print()
    
    try:
        test_root()
        print()
        
        # Uncomment the following lines to test full flow
        # seller_id = test_create_seller()
        # if seller_id:
        #     product_id = test_create_product(seller_id)
        #     test_get_products()
        #     test_cart_operations()
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure it's running with:")
        print("uvicorn main:app --reload")