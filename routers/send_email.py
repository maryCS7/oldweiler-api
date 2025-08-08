import os
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import resend

router = APIRouter()

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")
if not resend.api_key:
    raise RuntimeError("Missing RESEND_API_KEY in environment variables")


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
        "from": "Oldweiler Custom Carpentry <info@oldweilercustomcarpentry.com>",
        "to": ["mary.schroth719@gmail.com"],
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
                We’ve received your message and appreciate you taking the time to get in touch.
                I’ll be reviewing your request soon and will follow up with you as quickly as possible.
              </p>
              <p style="font-size: 16px; line-height: 1.6;">
                In the meantime, feel free to check out recent projects or follow up by call or text.
              </p>
              <p style="margin-top: 30px;">— Aaron Oldweiler<br/>Oldweiler Custom Carpentry</p>
              <hr style="margin: 30px 0;" />
              <p style="font-size: 14px; color: #666;">Based in Attica, NY — serving the surrounding areas</p>
            </div>
        """

        resend.Emails.send({
            "from": "Oldweiler Custom Carpentry <info@oldweilercustomcarpentry.com>",
            "to": [data.email],
            "subject": "Thanks for contacting Oldweiler Custom Carpentry!",
            "html": confirmation_html,
            "text": (
                f"Hi {data.name},\n\nThanks for reaching out! Your message has been received, "
                "and I’ll be in touch soon.\n\n— Aaron Oldweiler\nOldweiler Custom Carpentry"
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