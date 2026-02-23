import requests
from app.config.config import settings


def send_otp_email(to_email: str, otp: str):
    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "from": settings.EMAIL_FROM,
            "to": to_email,
            "subject": "Your Password Reset OTP",
            "html": f"""
                <h2>Password Reset</h2>
                <p>Your OTP is:</p>
                <h1>{otp}</h1>
                <p>This code expires in 10 minutes.</p>
            """,
        },
    )

    if response.status_code >= 400:
        raise Exception("Failed to send email")
