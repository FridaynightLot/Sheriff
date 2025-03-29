from motor.motor_asyncio import AsyncIOMotorClient
from config.config import MONGO_URI, DB_NAME

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.users = self.db.users
        self.premium_users = self.db.premium_users
        
    async def get_user(self, user_id: int):
        return await self.users.find_one({'_id': user_id})
        
    async def create_user(self, user_id: int):
        user_data = {
            '_id': user_id,
            'balance': 0,
            'inventory': [],
            'daily_last_claim': None
        }
        await self.users.insert_one(user_data)
        return user_data
        
    async def get_or_create_user(self, user_id: int):
        user = await self.get_user(user_id)
        if not user:
            user = await self.create_user(user_id)
        return user
        
    async def update_balance(self, user_id: int, amount: int):
        await self.users.update_one(
            {'_id': user_id},
            {'$inc': {'balance': amount}}
        )
        
    async def add_premium_role(self, user_id: int, role_name: str, expires_at):
        await self.premium_users.update_one(
            {'_id': user_id},
            {
                '$set': {
                    'role': role_name,
                    'expires_at': expires_at
                }
            },
            upsert=True
        )
        
    async def remove_premium_role(self, user_id: int):
        await self.premium_users.delete_one({'_id': user_id})
        
    async def get_premium_status(self, user_id: int):
        return await self.premium_users.find_one({'_id': user_id})
        
    async def is_premium(self, user_id: int):
        status = await self.get_premium_status(user_id)
        return bool(status) 