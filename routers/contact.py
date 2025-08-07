from fastapi import APIRouter, HTTPException
from schemas import ContactForm
from routers.send_email import send_email

router = APIRouter(
    prefix="/contact",
    tags=["contact"]
)

@router.post("/")
def submit_contact_form(form: ContactForm):
    try:
        send_email(form)
        return {"message": "Contact form received and email sent!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email failed to send: {str(e)}")