from fastapi import HTTPException
from email.message import EmailMessage

import aiosmtplib
import MongoDB


async def SendEmailAsync(api_key: str, subject: str, body: str):
    recipient_email = await MongoDB.getEmail(api_key)
    sender_email = "nsanjaysagar205@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = "wesy nfyp cuei vibf"

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.set_content(body)

    try:
        await aiosmtplib.send(
            message,
            hostname=smtp_server,
            port=smtp_port,
            start_tls=True,
            username=smtp_username,
            password=smtp_password,
        )
        return {"message": "Email sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
