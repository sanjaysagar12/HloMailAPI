from fastapi import HTTPException
from email.message import EmailMessage
from pydantic import EmailStr

import aiosmtplib
import MongoDB
import secrets

sender_email = "nsanjaysagar205@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = sender_email
smtp_password = "wesy nfyp cuei vibf"


async def generate_secure_otp(length=6):
    # Generate a cryptographically secure OTP of the specified length
    otp = "".join([str(secrets.randbelow(10)) for _ in range(length)])
    return str(otp)


async def verifyOTP(EMAIL: EmailStr, ENTERED_OTP):
    OTP = await MongoDB.getOTP(EMAIL)
    print(OTP, ENTERED_OTP)
    if str(OTP) == str(ENTERED_OTP):
        return True
    return False


async def sendOTP(RECIPIENT_EMAIL: EmailStr):
    # Example usage
    OTP = await generate_secure_otp()
    await MongoDB.setOTP(RECIPIENT_EMAIL, OTP)
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = RECIPIENT_EMAIL
    message["Subject"] = "OTP"
    message.set_content(str(OTP))

    try:
        await aiosmtplib.send(
            message,
            hostname=smtp_server,
            port=smtp_port,
            start_tls=True,
            username=smtp_username,
            password=smtp_password,
        )
        MongoDB.getOTP(RECIPIENT_EMAIL)
        return {"message": f"OTP sent successfully! "}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")


async def sendEmailAsync(api_key: str, subject: str, body: str):
    recipient_email = await MongoDB.getEmail(api_key)

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
