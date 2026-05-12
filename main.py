from fastapi import FastAPI
from app.routers import products, cart, checkout

app = FastAPI(
    title="E-commerce API",
    description="A backend API for an e-commerce site that leads clients to sellers' WhatsApp with cart functionality",
    version="1.0.0"
)

# Include routers
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(checkout.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the E-commerce API",
        "docs": "/docs",
        "redoc": "/redoc"
    }