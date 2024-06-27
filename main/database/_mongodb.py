from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_URL

# function database
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client.cilik

akundb = db.akun

async def add_akuns(user_id, api_id, api_hash, session_string):
    return await akundb.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "api_id": api_id,
                "api_hash": api_hash,
                "session_string": session_string,
            }
        },
        upsert=True,
    )


async def get_all_akun():
    data = []
    async for akun in akundb.find({"user_id": {"$exists": 1}}):
        data.append(
            dict(
                name=str(akun["user_id"]),
                api_id=akun["api_id"],
                api_hash=akun["api_hash"],
                session_string=akun["session_string"],
            )
        )
    return data


async def get_akun(user_id):
    user_data = await akundb.find_one({"user_id": user_id})
    return user_data


async def remove_akun(user_id):
    return await akundb.delete_one({"user_id": user_id})

