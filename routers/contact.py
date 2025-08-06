from fastapi import APIRouter
from schemas import ContactForm

router = APIRouter(
    prefix="/contact",
    tags=["contact"]
)

@router.post("/")
def submit_contact_form(form: ContactForm):
    return {"message": "Contact form received!", "data": form}