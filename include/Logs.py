from collections import defaultdict
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

    async def get_todays_data(self, api_key=None, brief=False):
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

    async def get_weeks_data(self, api_key=None, brief=False):
        start_time = datetime.datetime.now() - datetime.timedelta(days=7)
        end_time = datetime.datetime.now()
        query = {"time": {"$gte": start_time, "$lte": end_time}}
        if api_key:
            query["api_key"] = api_key
        data = await self.logs_collection.get(query=query)
        if brief:
            return self._group_by_week(data)
        return self._make_serializable(data)

    async def get_months_data(self, api_key=None, brief=False):
        start_time = datetime.datetime.now() - datetime.timedelta(days=30)
        end_time = datetime.datetime.now()
        query = {"time": {"$gte": start_time, "$lte": end_time}}
        if api_key:
            query["api_key"] = api_key
        data = await self.logs_collection.get(query=query)
        if brief:
            return self._group_by_month(data)
        return self._make_serializable(data)

    async def get_years_data(self, api_key=None, brief=False):
        start_time = datetime.datetime.now() - datetime.timedelta(days=365)
        end_time = datetime.datetime.now()
        query = {"time": {"$gte": start_time, "$lte": end_time}}
        if api_key:
            query["api_key"] = api_key
        data = await self.logs_collection.get(query=query)
        if brief:
            return self._group_by_year(data)
        return self._make_serializable(data)

    def _make_serializable(self, data):
        # Convert datetime fields to ISO format string for JSON serialization
        for document in data:
            if "time" in document and isinstance(document["time"], datetime.datetime):
                document["time"] = document["time"].isoformat()
        return data

    def _group_by_month(self, data):
        month_counts = defaultdict(int)
        for document in data:
            month = document["time"].month
            month_counts[month] += 1
        return [month_counts]

    def _group_by_week(self, data):
        week_counts = defaultdict(int)
        for document in data:
            week = document["time"].isocalendar()[1]
            week_counts[week] += 1
        return [week_counts]

    def _group_by_year(self, data):
        year_counts = defaultdict(int)
        for document in data:
            year = document["time"].year
            year_counts[year] += 1
        return [year_counts]
