import aiosmtplib

from fastapi import HTTPException
from email.message import EmailMessage
from pydantic import EmailStr
from MongoDB import MongoDB

sender_email = "nsanjaysagar205@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = sender_email
smtp_password = "wesy nfyp cuei vibf"

user_collection = MongoDB("admin", "users")


class EMail:
    async def send_hlomail(
        self, user_email: EmailStr, recipient_email: EmailStr, subject: str, body: str
    ):

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
            result = await user_collection.set(
                increment_field="credit",
                increment_value=-1,
                where={"email": user_email},
            )  # Decrement credit by 1
            print(result)
            return {"message": "Email sent successfully!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

    async def send(self, recipient_email: EmailStr, subject: str, body: str):

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
