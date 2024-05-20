import datetime
import hashlib
import random
import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://root:12345@localhost:27017/")
database = client["admin"]
user_collection = database.get_collection("api_keys")


async def addService(EMAIL: str, SERVICE: str):

    current_datetime = datetime.datetime.now()
    api_key = str(
        hashlib.md5(
            f"{current_datetime}+{EMAIL}+{random.randint(0,1000)}".encode()
        ).hexdigest()
    )
    # Convert CreateUser instance to dictionary
    api_key_dict = {
        "api_key": api_key,
        "email": EMAIL,
        "service": SERVICE,
    }
    # Insert the user data into the database
    result = await user_collection.insert_one(api_key_dict)
    # Return the inserted user ID
    return {"api_key": api_key}


async def getEmail(api_key: str):
    user_data = await user_collection.find_one({"api_key": api_key})
    if user_data:
        return user_data["email"]
    return None
