import datetime
import json
import secrets
from .MongoDB import MongoDB

api_keys_collection = MongoDB("admin", "api_keys")


class APIKey:
    def __init__(self, email=None) -> None:
        self.email = email

    async def generate_key(self, api_type, title, desc=None):
        api_key = secrets.token_hex(16)
        created_on = datetime.datetime.now()
        await api_keys_collection.set(
            {
                "title": title,
                "desc": desc,
                "email": self.email,
                "api_key": api_key,
                "type": api_type,
                "created_on": created_on,
            }
        )
        return {"message": "Succesfully generated API Key", "api_key": api_key}

    async def set(self, key=None, value=None, where=None):
        where.update(
            {
                "email": self.email,
            }
        )
        data = await api_keys_collection.set(key=key, value=value, where=where)
        return data

    async def delete(self, api_key):
        return await api_keys_collection.delete(
            {"api_key": api_key, "email": self.email}
        )

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

            data = await api_keys_collection.get(query={"email": self.email})
            if data:
                data = json.dumps(data, default=serialize_datetime)
                data = json.loads(data)
                return {"data": data}
            else:
                return {"data": data}
        if data:
            return {"valid": True, "data": data}
        return {"valid": False, "error": "invalid api key"}
