import json

from .MongoDB import MongoDB

user_collection = MongoDB("hlomail_db", "users")


class User:
    def __init__(self, email) -> None:
        self.__dict__["email"] = email

    async def get(self, key=None):
        data = await user_collection.get(
            "email",
            self.__dict__["email"],
        )
        if key:
            return data[key]
        return data

    async def set(self, key, value=None):
        if value:
            await user_collection.set(
                key=key, value=value, where={"email": self.__dict__["email"]}
            )

        await user_collection.set(key)

    async def is_exist(self):
        user_data = await user_collection.get("email", self.__dict__["email"])
        if user_data:
            return True
        return False
