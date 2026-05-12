from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test negative price
response = client.post(
    "/products/",
    json={
        "name": "Test Product",
        "description": "A test product",
        "price": -10.0,  # Should be positive
        "seller_id": 1
    }
)
print(f"Status code: {response.status_code}")
print(f"Response: {response.json()}")