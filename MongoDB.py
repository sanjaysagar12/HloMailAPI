import datetime
import hashlib
import random
import motor.motor_asyncio
from pydantic import BaseModel, EmailStr


# Connecting To Database
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://root:12345@localhost:27017/")

database = client["admin"]
api_keys_collection = database.get_collection("api_keys")


async def getOTP(EMAIL: EmailStr):
    opt_collection = database.get_collection("otp")

    user_data = await opt_collection.find_one({"email": EMAIL})
    if user_data:
        return user_data["otp"]
    return None


async def setOTP(EMAIL: EmailStr, OTP: str):
    opt_collection = database.get_collection("otp")

    opt_data = await opt_collection.find_one({"email": EMAIL})
    if opt_data:
        myquery = {"email": EMAIL}
        newvalues = {"$set": {"otp": OTP}}
        await opt_collection.update_one(myquery, newvalues)

    else:
        otp_dict = {
            "email": EMAIL,
            "otp": OTP,
        }
        # Insert the OTP data into the database
        result = await opt_collection.insert_one(otp_dict)
    print("OTP Added")
    return None


# Adding New Service for User
async def addService(USER_EMAIL: str, SERVICE: str, PROJECT_NAME: str):

    current_datetime = datetime.datetime.now()
    api_key = str(
        hashlib.md5(
            f"{current_datetime}+{USER_EMAIL}+{random.randint(0,1000)}".encode()
        ).hexdigest()
    )
    # Convert CreateUser instance to dictionary
    api_key_dict = {
        "api_key": api_key,
        "email": USER_EMAIL,
        "service": SERVICE,
        "project_name": PROJECT_NAME,
        "created_on": current_datetime,
    }
    # Insert the user data into the database
    result = await api_keys_collection.insert_one(api_key_dict)
    # Return the inserted user ID
    return {"api_key": api_key}


# get Email From api_key
async def getEmail(api_key: str):
    api_key_data = await api_keys_collection.find_one({"api_key": api_key})
    if api_key_data:
        return api_key_data["email"]
    return None
