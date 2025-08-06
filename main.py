from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import review
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

@app.get("/")
def read_root():
    return {"message": "Hello from Oldweiler-Carpentry API!"}

@app.get("/test")
def test_api():
    return {"message": "Endpoint working! Yippeeee"}
    
# @app.post("/contact")
# def submit_contact(form: ContactForm):
#     print(f"New message from {form.name} ({form.email}): {form.message}")
#     return {"success": True, "message": "Message received"}