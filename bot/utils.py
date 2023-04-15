from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient

from bot.config import settings


CREATED_DATE = "$created_date"
ID = "$_id"

client = AsyncIOMotorClient(
    settings.mongo_host.get_secret_value(),
    settings.mongo_port
)

mongo_db = settings.mongo_db.get_secret_value()
mongo_db_col = settings.mongo_db_col.get_secret_value()
collection = client[mongo_db][mongo_db_col]


async def get_group_salary_data(
    dt_from_iso: str,
    dt_upto_iso: str,
    group_type: str,
) -> dict[str, list[datetime | int]]:
    def fill_date_parts(data_field: str):
        data = dict(
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
                "dt": {
                    "$gte": dt_from,
                    "$lte": dt_upto,
                },
            },
        },
        {
            "$addFields": {
                "created_date": {
                    "$dateToParts": {
                            "date": {
                                "$toDate": {"$toLong": "$dt"},
                            },
                        },
                },
            },
        },
        {
            "$group": {
                "_id": fill_date_parts(data_field=CREATED_DATE),
                "total": {"$sum": "$value"},
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

    cursor = collection.aggregate(pipeline)
    async for document in cursor:
        result["dataset"].append(document["total"])
        result["labels"].append(document["date"].isoformat())

    print(result)
    return result
