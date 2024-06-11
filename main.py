import json
import os
import datetime
from typing import Optional
import sys
import aiohttp
from fastapi import FastAPI, Header, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, ValidationError
from fastapi.responses import JSONResponse
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from pydantic import EmailStr

# Add this line to import URLSafeTimedSerializer
from itsdangerous import URLSafeTimedSerializer

from include.Logs import Logs
from include.MongoDB import MongoDB
from include.User import User
from include.Session import Session
from include.Authentication import Authentication
from include.EMail import EMail
from include.API import APIKey

root_path = os.path.dirname(__file__)

# Initialize FastAPI
app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:5173",  # Assuming your React app runs on port 5173
    "https://hlomail-frontend.sanjaysagar.com/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Token"],
)


SECRET_KEY = "your-secret-key"  # Change this to your actual secret key
PASSWORD_RESET_TOKEN_EXPIRY = 3600  # Token expiry time in seconds (e.g., 1 hour)

serializer = URLSafeTimedSerializer(SECRET_KEY)

from pydantic import BaseModel
from passlib.context import CryptContext


email = EMail()
session = Session()
api_types = ("contact", "noreply")


# Pydantic models
class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class VerifyRequest(BaseModel):
    email: EmailStr
    otp: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ResetPasswordRequest(BaseModel):
    new_password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class AddApiKeyRequest(BaseModel):
    api_type: str
    title: str
    desc: Optional[str] = None


class NoReplyMailRequest(BaseModel):
    api_key: str
    sender: str
    recipient: str
    recipient_email: EmailStr
    subject: str
    body: str


class ContactMailRequest(BaseModel):
    api_key: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str


class EditApiKeyRequest(BaseModel):
    api_key: str
    title: str
    desc: Optional[str] = None


class DeleteApiKeyRequest(BaseModel):
    api_key: str


class NoSignupRequest(BaseModel):
    email: EmailStr


async def get_token_header(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=400, detail="Authorization header missing")

    # Assuming the token is prefixed with "Bearer "
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid authorization format")

    token = authorization[len("Bearer ") :]
    return token


async def verify_session(token: str, client_ip: str, user_agent: str):
    if token is None:
        raise HTTPException(status_code=401, detail="Token is missing")

    return await session.verify(token, client_ip=client_ip, user_agent=user_agent)


@app.post("/register")
async def register_user(request_model: RegisterRequest):

    auth = Authentication()
    response = await auth.register(
        request_model.email, request_model.username, request_model.password
    )

    if response["valid"]:
        otp = response["otp"]
        await email.send(
            recipient_email=request_model.email,
            subject="OTP",
            body=str(otp),
        )
        return JSONResponse(
            content={
                "valid": True,
                "message": "User registered successfully, please verify OTP sent to email.",
            }
        )

    return JSONResponse(content=response)


@app.post("/verify")
async def verify_user(request_model: VerifyRequest):

    auth = Authentication()
    result = await auth.verify(request_model.email, request_model.otp)
    return JSONResponse(content=result)


@app.post("/login")
async def login_user(request: Request, request_model: LoginRequest):

    auth = Authentication()
    response = await auth.login(request_model.email, request_model.password)

    if response["valid"]:
        session = Session()
        user = User(request_model.email)
        token = await session.start()
        client_ip = request.client.host
        user_agent = request.headers.get("User-Agent")

        created_on = datetime.datetime.now()
        expire_on = created_on + datetime.timedelta(days=10)

        # To prevent session hijacking
        await session.set("email", request_model.email)
        await session.set("client_ip", client_ip)
        await session.set("user_agent", user_agent)
        await session.set("username", await user.get("username"))

        await session.set("created_on", str(created_on))
        await session.set("expire_on", str(expire_on))
        response.update({"token": token["token"]})
        return JSONResponse(content=response)

    raise HTTPException(status_code=401, detail=response)


@app.post("/forgot-password")
async def forgot_password(request: Request, request_model: ForgotPasswordRequest):

    user = User(request_model.email)

    if not await user.is_exist():
        raise HTTPException(status_code=404, detail="User not found")

    token = serializer.dumps(request_model.email, salt="password-reset-salt")
    reset_link = f"http://localhost:8000/reset-password?token={token}"

    await email.send(
        recipient_email=request_model.email,
        subject="OTP",
        body=str(reset_link),
    )

    return JSONResponse(content={"message": "Password reset link sent to your email"})


@app.post("/reset-password")
async def reset_password(request: Request, token: str):

    try:
        data = await request.json()
        request_model = ResetPasswordRequest(**data)
    except (ValidationError, TypeError) as e:
        raise HTTPException(status_code=401, detail=str(e))

    try:
        email = serializer.loads(
            token,
            salt="password-reset-salt",
            max_age=PASSWORD_RESET_TOKEN_EXPIRY,
        )
    except SignatureExpired:
        raise HTTPException(status_code=401, detail="Token expired")
    except BadSignature:
        raise HTTPException(status_code=401, detail="Invalid token")
    authentication_collection = MongoDB("admin", "authentication")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    hashed_password = pwd_context.hash(request_model.new_password)
    await authentication_collection.set(
        key="password",
        value=hashed_password,
        where={"email": email},
    )

    return JSONResponse(content={"message": "Password reset successfully"})


@app.post("/profile")
async def profile(request: Request, token: str = Depends(get_token_header)):
    # verifying the session

    client_ip = request.client.host
    user_agent = request.headers.get("User-Agent")
    result = await verify_session(
        token=token,
        client_ip=client_ip,
        user_agent=user_agent,
    )

    if result["valid"]:
        user = User(await session.get("email"))
        return JSONResponse(
            content={
                "valid": True,
                "message": "Token is valid.",
                "username": await user.get("username"),
                "session_data": result["session_data"],
                "user_data": await user.get(),
                "client_ip": client_ip,
            }
        )

    raise HTTPException(status_code=401, detail=result["error"])


@app.post("/dashboard")
async def dashboard(request: Request, token: str = Depends(get_token_header)):

    # verifying the session

    client_ip = request.client.host
    user_agent = request.headers.get("User-Agent")
    result = await verify_session(
        token=token,
        client_ip=client_ip,
        user_agent=user_agent,
    )
    if result["valid"]:
        email = await session.get("email")
        api_key = APIKey(email)
        response = await api_key.get()
        response.update({"valid": True})
        return JSONResponse(response)
    raise HTTPException(status_code=401, detail=result["error"])


@app.post("/add-apikey")
async def add_apikey(
    request: Request,
    project_data: AddApiKeyRequest,
    token: str = Depends(get_token_header),
):
    # verifying the session

    client_ip = request.client.host
    user_agent = request.headers.get("User-Agent")

    result = await verify_session(
        token=token,
        client_ip=client_ip,
        user_agent=user_agent,
    )
    if project_data.api_type not in api_types:
        return {
            "valid": False,
            "error": "invalid api type",
        }

    if result["valid"]:
        api_key = APIKey(await session.get("email"))
        api_key_response = await api_key.generate_key(
            title=project_data.title,
            desc=project_data.desc,
            api_type=project_data.api_type,
        )
        api_key_response.update({"valid": True})
        return JSONResponse(
            api_key_response,
        )

    raise HTTPException(status_code=401, detail=result["error"])


@app.post("/edit-apikey")
async def edit_apikey(
    request: Request,
    project_data: EditApiKeyRequest,
    token: str = Depends(get_token_header),
):
    # verifying the session

    client_ip = request.client.host
    user_agent = request.headers.get("User-Agent")

    result = await verify_session(
        token=token,
        client_ip=client_ip,
        user_agent=user_agent,
    )

    if result["valid"]:
        api_key = APIKey(await session.get("email"))
        api_key_response = await api_key.set(
            key="title",
            value=project_data.title,
            where={"api_key": project_data.api_key},
        )
        api_key_response = await api_key.set(
            key="desc",
            value=project_data.desc,
            where={"api_key": project_data.api_key},
        )
        api_key_response.update({"valid": True})
        return JSONResponse(
            api_key_response,
        )

    raise HTTPException(status_code=401, detail=result["error"])


@app.post("/delete-apikey")
async def delete_apikey(
    request: Request,
    project_data: DeleteApiKeyRequest,
    token: str = Depends(get_token_header),
):
    # verifying the session
    client_ip = request.client.host
    user_agent = request.headers.get("User-Agent")

    result = await verify_session(
        token=token,
        client_ip=client_ip,
        user_agent=user_agent,
    )

    if result["valid"]:
        api_key = APIKey(await session.get("email"))
        api_key_response = await api_key.delete(api_key=project_data.api_key)
        api_key_response.update({"valid": True})
        return JSONResponse(
            api_key_response,
        )
    raise HTTPException(status_code=401, detail=result["error"])


class LogsRequest(BaseModel):
    api_key: Optional[str] = None
    time_period: str


@app.post("/logs")
async def logs(
    request: Request,
    logs_data: LogsRequest,
    token: str = Depends(get_token_header),
):
    # verifying the session
    client_ip = request.client.host
    user_agent = request.headers.get("User-Agent")

    result = await verify_session(
        token=token,
        client_ip=client_ip,
        user_agent=user_agent,
    )
    logs = Logs(await session.get("email"))
    if result["valid"]:

        if logs_data.time_period == "today":
            log_result = await logs.get_todays_data(logs_data.api_key)
        elif logs_data.time_period == "week":
            log_result = await logs.get_weeks_data(logs_data.api_key, brief=True)
        elif logs_data.time_period == "month":
            log_result = await logs.get_months_data(logs_data.api_key, brief=True)
        elif logs_data.time_period == "year":
            log_result = await logs.get_years_data(logs_data.api_key, brief=True)
        print("log_result:", log_result)
        return JSONResponse({"valid": True, "log_result": log_result})


@app.post("/contact-mail")
async def contact_mail(
    contact_data: ContactMailRequest,
):

    api_key = APIKey()
    api_key_response = await api_key.get(key="api_key", value=contact_data.api_key)
    print(api_key_response)
    if api_key_response["valid"]:
        api_key_data = api_key_response["data"]
        if api_key_data["type"] == "contact":
            respose = await email.send_hlomail(
                recipient_email=api_key_data["email"],
                subject=contact_data.name + "Contacted You",
                body=contact_data.email,
                user_email=api_key_data["email"],
            )
            logs = Logs(await session.get("email"))
            await logs.set(api_key=contact_data.api_key)
            respose.update({"valid": True})
            return JSONResponse(
                respose,
            )
        raise HTTPException(
            status_code=401,
            detail="your api token type is not sutable for contact mail",
        )

    raise HTTPException(status_code=401, detail=api_key_response["error"])


@app.post("/noreply-mail")
async def noreply_mail(
    noreply_data: NoReplyMailRequest,
):

    api_key = APIKey()
    api_key_response = await api_key.get(key="api_key", value=noreply_data.api_key)

    if api_key_response["valid"]:
        api_key_data = api_key_response["data"]
        if api_key_data["type"] == "noreply":
            respose = await email.send_hlomail(
                recipient_email=noreply_data.recipient_email,
                subject=noreply_data.subject,
                body=noreply_data.body,
                user_email=api_key_data["email"],
            )
            respose.update({"valid": True})
            logs = Logs(await session.get("email"))
            await logs.set(api_key=noreply_data.api_key)
            return JSONResponse(
                respose,
            )
        raise HTTPException(
            status_code=401,
            detail="your api token type is not sutable for noreplay mail",
        )

    raise HTTPException(status_code=401, detail=api_key_response["error"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
