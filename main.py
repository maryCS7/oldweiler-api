import os
import logging
import time
from collections import defaultdict
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers import review, send_email
from schemas import ContactForm
from routers import contact

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.getenv("ENV") == "production" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log") if os.getenv("ENV") == "production" else None
    ]
)
logger = logging.getLogger(__name__)

# Rate limiting configuration
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))  # Max requests per window
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # Time window in seconds (default: 1 hour)

# In-memory storage for rate limiting (simple but effective)
request_counts = defaultdict(list)

def check_rate_limit(request: Request):
    """Check if request exceeds rate limit"""
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old requests outside the time window
    request_counts[client_ip] = [
        req_time for req_time in request_counts[client_ip] 
        if current_time - req_time < RATE_LIMIT_WINDOW
    ]
    
    # Check if limit exceeded
    if len(request_counts[client_ip]) >= RATE_LIMIT_REQUESTS:
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(
            status_code=429, 
            detail=f"Rate limit exceeded. Maximum {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW} seconds."
        )
    
    # Add current request
    request_counts[client_ip].append(current_time)

app = FastAPI(title="Oldweiler Custom Carpentry API", version="1.0.0")

# Get allowed origins from environment, default to development
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

logger.info(f"Starting API with allowed origins: {ALLOWED_ORIGINS}")
logger.info(f"Rate limiting: {RATE_LIMIT_REQUESTS} requests per {RATE_LIMIT_WINDOW} seconds")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contact.router)
app.include_router(review.router)
app.include_router(send_email.router)

@app.get("/")
def read_root():
    return {"message": "Hello from Oldweiler-Carpentry API!"}

@app.get("/test")
def test_api():
    return {"message": "Endpoint working! Yippeeee"}

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms to monitor app status"""
    import time
    from sqlalchemy import text
    
    start_time = time.time()
    
    try:
        # Check database connection
        from database import get_db
        db = next(get_db())
        db.execute(text("SELECT 1"))  # Use text() for raw SQL
        db.close()
        
        response_time = round((time.time() - start_time) * 1000, 2)  # Convert to milliseconds
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "response_time_ms": response_time,
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": time.time(),
            "error": str(e),
            "database": "disconnected"
        }, 500

@app.get("/init-db")
async def initialize_database():
    """Initialize database tables (for production setup)"""
    try:
        from models import Review
        from database import engine
        
        # Create all tables
        Review.metadata.create_all(bind=engine)
        
        logger.info("Database tables created successfully")
        return {
            "status": "success",
            "message": "Database tables created successfully",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize database: {str(e)}"
        )
