from email.utils import formataddr
import json
import os
import aiosmtplib
import asyncio

from fastapi import HTTPException
from email.message import EmailMessage
from pydantic import EmailStr
from .MongoDB import MongoDB
from .EmailTemplates import EmailContactTemplates, EmailNoreplyTemplates

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
    async def send_email_to_recipient(self,sender, recipient_email, subject, body):
        message = EmailMessage()
        message["From"] = formataddr((sender, sender))
        message["To"] = formataddr((recipient_email, recipient_email))
        message["Subject"] = subject
        message.add_alternative(body, subtype="html")

        try:
            await aiosmtplib.send(
                message,
                hostname=smtp_server,
                port=smtp_port,
                start_tls=True,
                username=smtp_username,
                password=smtp_password,
            )
            return True
        except aiosmtplib.errors.SMTPException as e:
            print(f"Failed to send email to {recipient_email}: {e}")
            return False
        except Exception as e:
            print(f"An error occurred for {recipient_email}: {e}")
            return False

    async def send_noreply_hlomail(self, sender, mail_data):
        """Send emails and decrement user's credit by 1 for each email sent successfully."""
        subject = mail_data.subject
        contact_templates = EmailNoreplyTemplates()
        api_title = "Your API Title"  # Assuming api_title is a known variable

        if not mail_data.template:
            body = contact_templates.cleanProfessional(mail_data)
        elif mail_data.template == "1":
            body = contact_templates.cleanProfessional(api_title, mail_data)
        elif mail_data.template == "2":
            body = contact_templates.modernMinimalist(api_title, mail_data)
        elif mail_data.template == "3":
            body = contact_templates.elegantStylish(api_title, mail_data)
        elif mail_data.template == "4":
            body = contact_templates.classicFormal(api_title, mail_data)
        elif mail_data.template == "5":
            body = contact_templates.vibrantEnergetic(api_title, mail_data)
        elif mail_data.template == "6":
            body = contact_templates.boldVibrant(api_title, mail_data)
        elif mail_data.template == "7":
            body = contact_templates.softCalm(api_title, mail_data)
        elif mail_data.template == "8":
            body = contact_templates.luxuriousElegant(api_title, mail_data)
        elif mail_data.template == "9":
            body = contact_templates.funFriendly(api_title, mail_data)
        elif mail_data.template == "10":
            body = contact_templates.sleekModern(api_title, mail_data)
        else:
            body = contact_templates.cleanProfessional( mail_data)

        tasks = [
            self.send_email_to_recipient(sender, recipient_email, subject, body)
            for recipient_email in mail_data.recipient_email
        ]
        results = await asyncio.gather(*tasks)

        successful_emails = results.count(True)

        if successful_emails > 0:
            try:
                result = await user_collection.set(
                    increment_field="credit",
                    increment_value=-successful_emails,
                    where={"email": sender},
                )
                print(result)
                return {
                    "message": f"Email sent successfully to {successful_emails} recipients!"
                }
            except Exception as e:
                print(f"An error occurred while updating credits: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"An error occurred while updating credits: {e}",
                )
        else:
            raise HTTPException(status_code=500, detail="Failed to send any email")

    async def send_contact_hlomail(
        self, recipient_email: EmailMessage, api_title: str, mail_data: dict
    ):
        """Send an email and decrement user's credit by 1."""
        subject = f"New Intraction in {api_title}"
        message = EmailMessage()
        message["From"] = formataddr(("HloMail", "HloMail"))
        message["To"] = formataddr((recipient_email, recipient_email))
        message["Subject"] = subject
        body = ""
        contact_templates = EmailContactTemplates()
        if not mail_data.template:
            print("default")
            body = contact_templates.classicFormal(api_title, mail_data)
        elif mail_data.template == "1":
            print("1st")
            body = contact_templates.cleanProfessional(api_title, mail_data)
        elif mail_data.template == "2":
            print("2nd")
            body = contact_templates.modernMinimalist(api_title, mail_data)
        elif mail_data.template == "3":
            print("3rd")
            body = contact_templates.elegantStylish(api_title, mail_data)
        elif mail_data.template == "4":
            print("4th")
            body = contact_templates.classicFormal(api_title, mail_data)
        elif mail_data.template == "5":
            print("5th")
            body = contact_templates.vibrantEnergetic(api_title, mail_data)
        elif mail_data.template == "6":
            print("6th")
            body = contact_templates.boldVibrant(api_title, mail_data)
        elif mail_data.template == "7":
            print("7th")
            body = contact_templates.softCalm(api_title, mail_data)
        elif mail_data.template == "8":
            print("8th")
            body = contact_templates.luxuriousElegant(api_title, mail_data)
        elif mail_data.template == "9":
            print("9th")
            body = contact_templates.funFriendly(api_title, mail_data)
        elif mail_data.template == "10":
            print("10th")
            body = contact_templates.sleekModern(api_title, mail_data)
        else:
            print("not found")
            body = contact_templates.classicFormal(api_title, mail_data)
        message.add_alternative(
            body,
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
                where={"email": recipient_email},
            )
            print(result)
            return {"message": "Email sent successfully!"}
        except aiosmtplib.errors.SMTPException as e:
            print(f"Failed to send email: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    async def send(
        self,  recipient_email: EmailStr, subject: str, body: str
    ):
        """Send an email and decrement user's credit by 1."""

        message = EmailMessage()
        message["From"] = formataddr(("Sender Name", host_email))
        message["To"] = formataddr(("Recipient Name", recipient_email))
        message["Subject"] = subject

        message.add_alternative(
            f"""
              <html>
                <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.5; color: #333;">
                    <h1 style="color: #2196F3; text-align: center;">Hello,</h1>
                    <p style="text-align: center;">Thanks for registering in  <strong>hlomail</strong> </p>
                        <p><strong>OTP:</strong></p>
                        <p>{body}</p>
                    </div>
                    <br>
                    <p style="text-align: center;">Best regards,<br>HloMail Team</p>
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

        
            return {"message": "Email sent successfully!"}
        except aiosmtplib.errors.SMTPException as e:
            print(e)
            raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
        except Exception as e:

            print(e)
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    # async def send(self, recipient_email: EmailStr, subject: str, body: str):
    #     """Send an email."""

    #     message = EmailMessage()
    #     message["From"] = host_email
    #     message["To"] = recipient_email
    #     message["Subject"] = subject
    #     message.set_content(body)

    #     try:
    #         # Send email
    #         await aiosmtplib.send(
    #             message,
    #             hostname=smtp_server,
    #             port=smtp_port,
    #             start_tls=True,
    #             username=smtp_username,
    #             password=smtp_password,
    #         )
    #         return {"message": "Email sent successfully!"}
    #     except aiosmtplib.errors.SMTPException as e:
    #         raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
