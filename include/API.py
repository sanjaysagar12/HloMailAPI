import datetime
import json
import secrets
from MongoDB import MongoDB

api_keys_collection = MongoDB("admin", "api_keys")


class APIKey:
    def __init__(self, email=None) -> None:
        self.__dict__["email"] = email

    async def generate_key(self, title, desc=None):
        api_key = secrets.token_hex(16)
        created_on = datetime.datetime.now()
        await api_keys_collection.set(
            {
                "title": title,
                "desc": desc,
                "email": self.__dict__["email"],
                "api_key": api_key,
                "created_on": created_on,
            }
        )
        return {"message": "Succesfully generated API Key", "api_key": api_key}

    async def get(self, key=None, value=None):
        def serialize_datetime(obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            raise TypeError("Type not serializable")

        if key:
            data = await api_keys_collection.get(key=key, value=value)
            data = json.dumps(data, default=serialize_datetime)
            data = json.loads(data)
        else:

            data = await api_keys_collection.get(
                query={"email": self.__dict__["email"]}
            )
            if data:
                data = json.dumps(data, default=serialize_datetime)
                data = json.loads(data)
                return {"data": data}
            else:
                return {"data": data}
        if data:
            return {"valid": True, "data": data}
        return {"valid": False, "error": "invalid api key"}
