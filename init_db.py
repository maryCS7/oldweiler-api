from database import engine
from models import Review

# Create all tables
def init_db():
    Review.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db() 