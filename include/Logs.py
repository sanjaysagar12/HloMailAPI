import datetime
import json
from MongoDB import MongoDB


class Logs:
    def __init__(self, email) -> None:
        self.logs_collection = MongoDB("admin", f"{email}-logs")

    async def get(self, query):
        data = await self.logs_collection.get(query=query)
        return self._make_serializable(data)

    async def set(self, api_key, type, to=None):
        log_data = {
            "api_key": api_key,
            "type": type,
            "time": datetime.datetime.now(),
        }
        if to:
            log_data["to"] = to
        await self.logs_collection.set(key=log_data)

    async def get_todays_data(self):
        start_time = datetime.datetime.combine(
            datetime.datetime.today(), datetime.datetime.min.time()
        )
        end_time = datetime.datetime.combine(
            datetime.datetime.today(), datetime.datetime.max.time()
        )
        data = await self.logs_collection.get(
            query={"time": {"$gte": start_time, "$lte": end_time}}
        )
        return self._make_serializable(data)

    async def get_weeks_data(self):
        start_time = datetime.datetime.now() - datetime.timedelta(days=7)
        end_time = datetime.datetime.now()
        data = await self.logs_collection.get(
            query={"time": {"$gte": start_time, "$lte": end_time}}
        )
        return self._make_serializable(data)

    async def get_months_data(self):
        start_time = datetime.datetime.now() - datetime.timedelta(days=30)
        end_time = datetime.datetime.now()
        data = await self.logs_collection.get(
            query={"time": {"$gte": start_time, "$lte": end_time}}
        )
        return self._make_serializable(data)

    async def get_years_data(self):
        start_time = datetime.datetime.now() - datetime.timedelta(days=365)
        end_time = datetime.datetime.now()
        data = await self.logs_collection.get(
            query={"time": {"$gte": start_time, "$lte": end_time}}
        )
        return self._make_serializable(data)

    def _make_serializable(self, data):
        # Convert datetime fields to ISO format string for JSON serialization
        for document in data:
            if "time" in document and isinstance(document["time"], datetime.datetime):
                document["time"] = document["time"].isoformat()
        return data
