# redis_util.py

import redis.asyncio as aioredis

class RedisManager:
    def __init__(self):
        self.redis = None

    async def init(self):
        self.redis = aioredis.Redis(host="localhost", decode_responses=True)

    async def increase_question_count(self, user_token: str, interview_id: int) -> int:
        key = f"user:{user_token}:interview:{interview_id}:count"
        return await self.redis.incr(key)

    async def get_question_count(self, user_token: str, interview_id: int) -> int:
        key = f"user:{user_token}:interview:{interview_id}:count"
        value = await self.redis.get(key)
        return int(value or 0)

    async def reset_count(self, user_token: str, interview_id: int) -> None:
        key = f"user:{user_token}:interview:{interview_id}:count"
        await self.redis.delete(key)

    async def mark_session_done(self, user_token: str, interview_id: int) -> None:
        key = f"user:{user_token}:interview:{interview_id}:done"
        await self.redis.set(key, "1")

    async def is_session_done(self, user_token: str, interview_id: int) -> bool:
        key = f"user:{user_token}:interview:{interview_id}:done"
        value = await self.redis.get(key)
        return value == "1"

# 싱글톤 객체
redis_manager = RedisManager()
