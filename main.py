from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import MongoDB
import MailAPI


app = FastAPI()


class AddNewServiceRequest(BaseModel):
    email: EmailStr
    service_type: str


class ContactEmailRequest(BaseModel):
    api_key: str
    subject: str
    body: str


@app.get("/get_email")
async def getEmail(api_key: str):
    return await MongoDB.getEmail(api_key)


@app.post("/add_service")
async def addService(service_data: AddNewServiceRequest):
    return await MongoDB.addService(service_data.email, service_data.service_type)


@app.post("/contact/")
async def contactEmail(email_request: ContactEmailRequest):
    return await MailAPI.SendEmailAsync(
        email_request.api_key, email_request.subject, email_request.body
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
