from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import review, send_email
from schemas import ContactForm
from routers import contact

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
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
