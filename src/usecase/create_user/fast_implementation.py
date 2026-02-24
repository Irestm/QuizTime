import json
from redis.asyncio import Redis
from api.pydantic.models import CreateUserSchema
from infrastructure.security.password import get_password_hash

class RedisFastCreateUserUseCase:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.queue_key = "registration_queue"

    async def execute(self, schema: CreateUserSchema) -> dict:
        schema.password = get_password_hash(schema.password)
        user_data = schema.model_dump()

        await self.redis.rpush(self.queue_key, json.dumps(user_data))

        return {"status": "queued", "msg": "User created asynchronously"}