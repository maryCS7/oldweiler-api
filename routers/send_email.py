import os
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import resend

router = APIRouter()

load_dotenv()

# Get configuration from environment variables with sensible defaults
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "info@oldweilercustomcarpentry.com")
TO_EMAIL = os.getenv("TO_EMAIL", "mary.schroth719@gmail.com")
COMPANY_NAME = os.getenv("COMPANY_NAME", "Oldweiler Custom Carpentry")
COMPANY_LOCATION = os.getenv("COMPANY_LOCATION", "Bennington, NY")

# Validate required configuration
if not RESEND_API_KEY:
    raise RuntimeError("Missing RESEND_API_KEY in environment variables")

resend.api_key = RESEND_API_KEY


class EmailRequest(BaseModel):
    name: str
    email: EmailStr
    message: str


def send_email_with_resend(data: EmailRequest):
    request_id = str(uuid.uuid4())

    print(f"[{request_id}] 📨 Contact form submission")
    print(f"[{request_id}] From: {data.name} <{data.email}>")
    print(f"[{request_id}] Message: {data.message}")

    email_payload = {
        "from": f"{COMPANY_NAME} <{FROM_EMAIL}>",
        "to": [TO_EMAIL],
        "reply_to": data.email,
        "subject": f"New contact form message from {data.name}",
        "html": (
            f"<p><strong>Name:</strong> {data.name}</p>"
            f"<p><strong>Email:</strong> {data.email}</p>"
            f"<p><strong>Message:</strong></p>"
            f"<p>{data.message}</p>"
        ),
        "text": (
            f"Name: {data.name}\n"
            f"Email: {data.email}\n"
            f"Message:\n{data.message}"
        ),
    }

    try:
        response = resend.Emails.send(email_payload)
        print(f"[{request_id}] ✅ Email sent successfully. Resend response: {response}")
    except Exception as e:
        print(f"[{request_id}] ❌ Failed to send primary email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while sending your message. Please try again later."
        )

    # Send styled confirmation email to user
    try:
        confirmation_html = f"""
            <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f9fafb; color: #111;">
              <h2 style="color: #2563eb;">Thanks for reaching out, {data.name}!</h2>
              <p style="font-size: 16px; line-height: 1.6;">
                We've received your message and appreciate you taking the time to get in touch.
                I'll be reviewing your request soon and will follow up with you as quickly as possible.
              </p>
              
              <div style="background-color: #eff6ff; border-left: 4px solid #2563eb; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <h3 style="color: #1e40af; margin-top: 0;">While You Wait:</h3>
                <p style="margin-bottom: 15px;">
                  <strong>📱 Call or Text:</strong> <a href="tel:+15857345068" style="color: #2563eb; text-decoration: none;">(585) 734-5068</a>
                </p>
                <p style="margin-bottom: 15px;">
                  <strong>🌐 View My Work:</strong> <a href="https://oldweilercustomcarpentry.com/projects" style="color: #2563eb; text-decoration: none;">Browse Recent Projects</a>
                </p>
                <p style="margin-bottom: 0;">
                  <strong>📸 Gallery:</strong> <a href="https://oldweilercustomcarpentry.com/gallery" style="color: #2563eb; text-decoration: none;">See Finished Work</a>
                </p>
              </div>
              
              <div style="background-color: #f3f4f6; border: 1px solid #d1d5db; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <h3 style="color: #374151; margin-top: 0;">Your Message:</h3>
                <p style="font-style: italic; color: #4b5563; margin: 0;">"{data.message}"</p>
              </div>
              
              <p style="font-size: 16px; line-height: 1.6;">
                I typically respond within 48 hours, but feel free to reach out directly if you have urgent questions.
              </p>
              
              <p style="margin-top: 30px;">— Aaron Oldweiler<br/>{COMPANY_NAME}</p>
              <hr style="margin: 30px 0;" />
              <p style="font-size: 14px; color: #666;">Based in {COMPANY_LOCATION} — serving the surrounding areas</p>
            </div>
        """

        resend.Emails.send({
            "from": f"{COMPANY_NAME} <{FROM_EMAIL}>",
            "to": [data.email],
            "subject": "Thanks for contacting Oldweiler Custom Carpentry!",
            "html": confirmation_html,
            "text": (
                f"Hi {data.name},\n\n"
                f"Thanks for reaching out! Your message has been received, and I'll be in touch soon.\n\n"
                f"While you wait:\n"
                f"📱 Call or Text: (585) 734-5068\n"
                f"🌐 View My Work: https://oldweilercustomcarpentry.com/projects\n"
                f"📸 Gallery: https://oldweilercustomcarpentry.com/gallery\n\n"
                f"Your Message:\n"
                f'"{data.message}"\n\n'
                f"I typically respond within 48 hours, but feel free to reach out directly if you have urgent questions.\n\n"
                f"— Aaron Oldweiler\n{COMPANY_NAME}"
            ),
        })
        print(f"[{request_id}] ✅ Confirmation email sent to user")
    except Exception as e:
        print(f"[{request_id}] ⚠️ Failed to send confirmation email: {e}")

    return {"message": "Emails sent successfully", "request_id": request_id}


# Optional direct-access route
@router.post("/send-email")
async def send_email_route(data: EmailRequest):
    send_email_with_resend(data)
    return {"message": "Email sent successfully (direct endpoint)"}