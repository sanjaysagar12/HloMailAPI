from email.utils import formataddr
import json
import os
import aiosmtplib

from fastapi import HTTPException
from email.message import EmailMessage
from pydantic import EmailStr
from .MongoDB import MongoDB


# Define the root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Load configuration from config.json
config_path = os.path.join(root_path, "config.json")
with open(config_path, "r") as config_file:
    config = json.load(config_file)

# Extract database configuration
smtp_config = config["smtp"]
host_email = smtp_config["host_email"]
smtp_server = smtp_config["smtp_server"]
smtp_port = smtp_config["smtp_port"]
smtp_username = smtp_config["smtp_username"]
smtp_password = smtp_config["smtp_password"]


user_collection = MongoDB("admin", "users")


class EMail:
    async def send_hlomail(
        self, user_email: EmailStr, recipient_email: EmailStr, subject: str, body: str
    ):
        """Send an email and decrement user's credit by 1."""

        message = EmailMessage()
        message["From"] = formataddr(("Sender Name", host_email))
        message["To"] = formataddr(("Recipient Name", recipient_email))
        message["Subject"] = subject

        message.add_alternative(
            f"""
    <html>
        <body>
            <h1>Hello,</h1>
            <p>{body}</p>
        </body>
    </html>
    """,
            subtype="html",
        )

        try:
            # Send email
            await aiosmtplib.send(
                message,
                hostname=smtp_server,
                port=smtp_port,
                start_tls=True,
                username=smtp_username,
                password=smtp_password,
            )

            # Decrement user credit
            result = await user_collection.set(
                increment_field="credit",
                increment_value=-1,
                where={"email": user_email},
            )
            print(result)
            return {"message": "Email sent successfully!"}
        except aiosmtplib.errors.SMTPException as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    async def send(self, recipient_email: EmailStr, subject: str, body: str):
        """Send an email."""

        message = EmailMessage()
        message["From"] = host_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.set_content(body)

        try:
            # Send email
            await aiosmtplib.send(
                message,
                hostname=smtp_server,
                port=smtp_port,
                start_tls=True,
                username=smtp_username,
                password=smtp_password,
            )
            return {"message": "Email sent successfully!"}
        except aiosmtplib.errors.SMTPException as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
