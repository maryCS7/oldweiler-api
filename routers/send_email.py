from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import resend
from dotenv import load_dotenv

router = APIRouter()

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

class EmailRequest(BaseModel):
    name: str
    email: str
    message: str

@router.post("/send-email")
async def send_email(data: EmailRequest):
    print("📨 Incoming contact form submission:")
    print(f"Name: {data.name}")
    print(f"Email: {data.email}")
    print(f"Message: {data.message}")

    email_payload = {
        "from": "info@oldweilercustomcarpentry.com",  
        "to": ["mary.schroth719@gmail.com"],          
        "reply_to": data.email,                        
        "subject": f"New contact form message from {data.name}",
        "html": f"""
            <p><strong>Name:</strong> {data.name}</p>
            <p><strong>Email:</strong> {data.email}</p>
            <p><strong>Message:</strong></p>
            <p>{data.message}</p>
        """,
        "text": f"Name: {data.name}\nEmail: {data.email}\nMessage:\n{data.message}"
    }

    try:
        response = resend.Emails.send(email_payload)

        print("✅ Resend API response:", response)
        return {
            "message": "Email sent successfully.",
            "resend_response": response
        }

    except Exception as e:
        print("❌ Error sending email:", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")