import requests
from app.config.config import settings

html= f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=DM+Sans:wght@400;500&display=swap');
            </style>
        </head>
        <body style="margin: 0; padding: 0; background-color: #fdf4ff; font-family: 'DM Sans', Helvetica, Arial, sans-serif;">
            
            <!-- Main Wrapper -->
            <div style="max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 24px; overflow: hidden; box-shadow: 0 4px 20px rgba(124, 58, 237, 0.08); border: 1px solid #f3e8ff;">
                
                <!-- Decorative Header Bar -->
                <div style="height: 8px; width: 100%; background: linear-gradient(90deg, #c084fc 0%, #7c3aed 100%);"></div>
                
                <div style="padding: 40px 40px;">
                    <!-- Icon / Brand -->
                    <div style="text-align: center; margin-bottom: 20px;">
                        <span style="display: inline-block; width: 48px; height: 48px; line-height: 48px; border-radius: 50%; background-color: #f3e8ff; color: #7c3aed; font-size: 24px;">✦</span>
                    </div>

                    <!-- Title -->
                    <h2 style="margin: 0 0 16px 0; color: #1f2937; text-align: center; font-family: 'Cormorant Garamond', Georgia, serif; font-size: 32px; font-weight: 600;">
                        Password Reset
                    </h2>

                    <!-- Body Text -->
                    <p style="margin: 0 0 24px 0; color: #6b7280; text-align: center; font-size: 16px; line-height: 1.6;">
                        We received a request to reset the password for your Vault. Use the code below to complete the process.
                    </p>

                    <!-- OTP Box -->
                    <div style="margin: 32px 0; text-align: center;">
                        <div style="display: inline-block; background-color: #faf5ff; border: 1px dashed #d8b4fe; border-radius: 12px; padding: 16px 32px;">
                            <span style="font-family: 'DM Sans', monospace; font-size: 36px; font-weight: 700; color: #7c3aed; letter-spacing: 6px;">
                                {otp}
                            </span>
                        </div>
                    </div>

                    <!-- Expiry Warning -->
                    <p style="margin: 0; text-align: center; color: #9ca3af; font-size: 14px;">
                        This code expires in <strong>10 minutes</strong>.
                    </p>
                </div>

                <!-- Footer -->
                <div style="background-color: #fdfaff; padding: 20px; text-align: center; border-top: 1px solid #f3e8ff;">
                    <p style="margin: 0; color: #9ca3af; font-size: 12px;">
                        If you didn't request this change, please ignore this email. <br>
                        Your memories are safe in the Vault.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

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
            "html":html,
        },
    )

    if response.status_code >= 400:
        raise Exception("Failed to send email")
