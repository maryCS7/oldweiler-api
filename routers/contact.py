import os
import logging
from fastapi import APIRouter, HTTPException, status
from schemas import ContactForm
from routers.send_email import send_email_with_resend

# Setup logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv("ENV") == "development" else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/contact",
    tags=["contact"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def submit_contact_form(form: ContactForm):
    env = os.getenv("ENV", "development")

    try:
        if env == "development":
            logger.debug(f"Received contact form: {form.dict()}")

        # Honeypot spam check
        if hasattr(form, "company") and form.company:
            logger.warning("Spam detected: Honeypot field was filled.")
            raise HTTPException(status_code=400, detail="Spam detected.")

        skip_email = os.getenv("SKIP_EMAIL", "false").lower() == "true"
        if not skip_email:
            send_email_with_resend(form)
            logger.info("Email successfully sent.")
        else:
            logger.info("Email sending skipped (dev mode).")

        return {"message": "Contact form received."}

    except Exception as e:
        logger.error(f"Email sending failed: {e}", exc_info=(env == "development"))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request."
        )