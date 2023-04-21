import json
import typing
from datetime import datetime, timedelta

import aiofiles
from motor.motor_asyncio import AsyncIOMotorClient

if typing.TYPE_CHECKING:
    from bot.bot import CustomBot


CREATED_DATE = "$created_date"
ID = "$_id"


class Mongo:
    def __init__(self, bot: "CustomBot"):
        self.bot = bot
        client = AsyncIOMotorClient(
            bot.config.mongo_host,
            bot.config.mongo_port,
        )
        db = client[bot.config.mongo_db]
        self.collection = db[bot.config.mongo_db_col]

    async def get_group_salary_data(
        self,
        tg_id: int,
        dt_from_iso: str,
        dt_upto_iso: str,
        group_type: str,
        date_field_name: str,
        value_field_name: str,
    ) -> dict[str, list[datetime | int]]:

        def fill_date_parts(data_field: str):
            data = dict(
                year=dict(
                    year=f"{data_field}.year",
                ),
                month=dict(
                    year=f"{data_field}.year",
                    month=f"{data_field}.month",
                ),
                day=dict(
                    year=f"{data_field}.year",
                    month=f"{data_field}.month",
                    day=f"{data_field}.day",
                ),
                hour=dict(
                    year=f"{data_field}.year",
                    month=f"{data_field}.month",
                    day=f"{data_field}.day",
                    hour=f"{data_field}.hour",
                ),
            )

            return data[group_type]

        dt_from = datetime.fromisoformat(dt_from_iso)
        dt_upto = datetime.fromisoformat(dt_upto_iso)

        pipeline = [
            {
                "$match": {
                    f"{date_field_name}": {
                        "$gte": dt_from,
                        "$lte": dt_upto,
                    },
                    "tg_id": {
                        "&eq": tg_id
                    }
                },
            },
            {
                "$addFields": {
                    "created_date": {
                        "$dateToParts": {
                            "date": {
                                "$toDate": {"$toLong": f"${date_field_name}"},
                            },
                        },
                    },
                },
            },
            {
                "$group": {
                    "_id": fill_date_parts(data_field=CREATED_DATE),
                    "total": {"$sum": f"${value_field_name}"},
                },
            },
            {
                "$project": {
                    "_id": 0,
                    "total": 1,
                    "date": {
                        "$dateFromParts": fill_date_parts(data_field=ID),
                    },
                },
            },
            {
                "$densify": {
                    "field": "date",
                    "range": {
                        "step": 1,
                        "unit": group_type,
                        "bounds": [dt_from, dt_upto + timedelta(seconds=1)],
                    },
                },
            },
            {
                "$set": {
                    "total": {
                        "$cond": [{"$not": ["$total"]}, 0, "$total"],
                    },
                },
            },
            {
                "$sort": {
                    "date": 1,
                },
            },
        ]

        result = dict(dataset=[], labels=[])

        cursor = self.collection.aggregate(pipeline)
        async for document in cursor:
            result["dataset"].append(document["total"])
            result["labels"].append(document["date"].isoformat())

        return result

    async def import_json_data(self, tg_id: int, chat_id: int, filename: str):
        async with aiofiles.open(filename) as f:
            async for line in f:
                doc = json.loads(line)
                doc["tg_id"] = tg_id
                await self.collection.insert_one(doc)
