import os
import motor.motor_asyncio
import json

# Define the root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Load configuration from config.json
config_path = os.path.join(root_path, "config.json")
with open(config_path, "r") as config_file:
    config = json.load(config_file)

# Extract database configuration
db_config = config["database"]
db_hostname = db_config["db_hostname"]
db_port = db_config["db_port"]
db_username = db_config["db_username"]
db_password = db_config["db_password"]
db_name = db_config["db_name"]

# Connecting to the Database
client = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb://{db_username}:{db_password}@{db_hostname}:{db_port}/hlomail_db?authSource=hlomail_db"
)

#  uri = f'mongodb://{username}:{password}@localhost:27017/hlomail_db?authSource=hlomail_db'

class MongoDB:
    def __init__(self, database: str, collection: str):
        self.database = client[database]
        self.collection = self.database.get_collection(collection)

    def get_connection(self):
        return self.collection

    async def is_exist(self, key: str, value):
        data = await self.get(key=key, value=value)
        return data is not None

    async def delete(self, query):

        result = await self.collection.delete_many(query)
        return (
            {"deleted": True}
            if result.deleted_count > 0
            else {"deleted": True, "error": "no documents found"}
        )

    async def set(
        self, key=None, value=None, where=None, increment_field=None, increment_value=0
    ):
        # Update data in Database
        if value is not None:
            print(key, value, where)
            if where is None:
                raise ValueError("The 'where' parameter is required for updating data.")
            newvalues = {"$set": {key: value}}
            result = await self.collection.update_many(where, newvalues)
            return (
                {"updated": True, "message": f"{key} updated to {value}"}
                if result.modified_count > 0
                else {"updated": False, "error": "no documents updated"}
            )

        # Increment or decrement a field
        if increment_field is not None and increment_value != 0:
            update = {"$inc": {increment_field: increment_value}}
            result = await self.collection.update_many(where, update)
            return (
                f"{increment_field} modified by {increment_value}"
                if result.modified_count > 0
                else "no documents modified"
            )

        # Add new data in Database
        result = await self.collection.insert_one(key)

        return f"new data inserted {key}"

    async def get(self, key: str = None, value=None, query: dict = None):
        if query:
            cursor = self.collection.find(query, {"_id": 0})
            results = []
            async for document in cursor:
                results.append(document)
            return results

        if key is not None and value is not None:
            return await self.collection.find_one({key: value}, {"_id": 0})

        raise ValueError("Either 'query' or both 'key' and 'value' must be provided.")
