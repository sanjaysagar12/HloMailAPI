import datetime
import json
from .MongoDB import MongoDB


class Logs:
    def __init__(self, email) -> None:
        self.logs_collection = MongoDB("admin", f"{email}-logs")

    async def get(self, query):
        data = await self.logs_collection.get(query=query)
        return self._make_serializable(data)

    async def set(self, api_key, type, time, to=None):
        log_data = {
            "api_key": api_key,
            "type": type,
            "time": time,
        }
        if to:
            log_data["to"] = to
        await self.logs_collection.set(key=log_data)

    async def get_todays_data(self, api_key=None):
        start_time = datetime.datetime.combine(
            datetime.datetime.today(), datetime.datetime.min.time()
        )
        end_time = datetime.datetime.combine(
            datetime.datetime.today(), datetime.datetime.max.time()
        )
        query = {"time": {"$gte": start_time, "$lte": end_time}}
        if api_key:
            query["api_key"] = api_key
        data = await self.logs_collection.get(query=query)
        return self._make_serializable(data)

    async def get_weeks_data(self, api_key=None):
        start_time = datetime.datetime.now() - datetime.timedelta(days=7)
        end_time = datetime.datetime.now()
        query = {"time": {"$gte": start_time, "$lte": end_time}}
        if api_key:
            query["api_key"] = api_key
        data = await self.logs_collection.get(query=query)
        return self._make_serializable(data)

    async def get_months_data(self, api_key=None):
        start_time = datetime.datetime.now() - datetime.timedelta(days=30)
        end_time = datetime.datetime.now()
        query = {"time": {"$gte": start_time, "$lte": end_time}}
        if api_key:
            query["api_key"] = api_key
        data = await self.logs_collection.get(query=query)
        return self._make_serializable(data)

    async def get_years_data(self, api_key=None):
        start_time = datetime.datetime.now() - datetime.timedelta(days=365)
        end_time = datetime.datetime.now()
        query = {"time": {"$gte": start_time, "$lte": end_time}}
        if api_key:
            query["api_key"] = api_key
        data = await self.logs_collection.get(query=query)
        return self._make_serializable(data)

    def _make_serializable(self, data):
        # Convert datetime fields to ISO format string for JSON serialization
        for document in data:
            if "time" in document and isinstance(document["time"], datetime.datetime):
                document["time"] = document["time"].isoformat()
        return data


# # Example usage (ensure to run in an async environment, like within an async function or event loop)
# import asyncio

# async def main():
#     logs = Logs('example_email')

#     # Insert test data with different timestamps
#     await logs.set('api_key_1', 'contact', datetime.datetime.now() - datetime.timedelta(days=365))
#     await logs.set('api_key_2', 'contact', datetime.datetime.now() - datetime.timedelta(days=30))
#     await logs.set('api_key_3', 'contact', datetime.datetime.now() - datetime.timedelta(days=10))

#     # Retrieve and print data for different periods
#     print("Today's data:", json.dumps(await logs.get_todays_data(), indent=4))
#     print("Last week's data:", json.dumps(await logs.get_weeks_data(), indent=4))
#     print("Last month's data:", json.dumps(await logs.get_months_data(), indent=4))
#     print("Last year's data:", json.dumps(await logs.get_years_data(), indent=4))

#     # Retrieve and print data for a specific API key within different periods
#     api_key = 'api_key_2'
#     print(f"Today's data for API key {api_key}:", json.dumps(await logs.get_todays_data(api_key), indent=4))
#     print(f"Last week's data for API key {api_key}:", json.dumps(await logs.get_weeks_data(api_key), indent=4))
#     print(f"Last month's data for API key {api_key}:", json.dumps(await logs.get_months_data(api_key), indent=4))
#     print(f"Last year's data for API key {api_key}:", json.dumps(await logs.get_years_data(api_key), indent=4))

# asyncio.run(main())
