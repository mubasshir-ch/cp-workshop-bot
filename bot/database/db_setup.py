from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    def __init__(self, uri):
        self.cluster = AsyncIOMotorClient(uri)
        self.db = self.cluster["cpworkshop"]
