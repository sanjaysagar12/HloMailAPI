from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import MongoDB
import MailAPI


app = FastAPI()


class AddNewServiceRequest(BaseModel):
    email: EmailStr
    service_type: str
    project_name: str


class ContactEmailRequest(BaseModel):
    api_key: str
    subject: str
    body: str


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str


@app.get("/get-email")
async def getEmail(api_key: str):
    return await MongoDB.getEmail(api_key)


@app.post("/verify-otp")
async def verityOTP(verification_data: VerifyOtpRequest):
    return await MailAPI.verifyOTP(verification_data.email, verification_data.otp)


@app.post("/generate-otp")
async def generateOTP(EMAIL: EmailStr):

    return await MailAPI.sendOTP(EMAIL)


@app.post("/add-service")
async def addService(service_data: AddNewServiceRequest):
    return await MongoDB.addService(
        USER_EMAIL=service_data.email,
        SERVICE=service_data.service_type,
        PROJECT_NAME=service_data.project_name,
    )


@app.post("/contact/")
async def contactEmail(email_request: ContactEmailRequest):
    return await MailAPI.sendEmailAsync(
        email_request.api_key, email_request.subject, email_request.body
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
