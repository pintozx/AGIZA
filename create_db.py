from app.database import engine, Base
from app import models  # Import models to ensure they are registered with Base

def create_database():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_database()