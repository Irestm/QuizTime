import asyncio
import json
import logging
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from settings import settings

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("Worker")

BATCH_SIZE = 1000
QUEUE_KEY = "registration_queue"

async def run_worker():
    db_url = settings.get_database_url() + "?prepared_statement_cache_size=0"
    logger.info(f"🔌 Connecting to DB via: {db_url}")

    redis_url = settings.get_redis_url()
    redis = Redis.from_url(redis_url)

    engine = create_async_engine(db_url, echo=False)

    logger.info("🚀 Worker Started. Waiting for users...")

    while True:
        try:
            async with redis.pipeline() as pipe:
                pipe.lrange(QUEUE_KEY, 0, BATCH_SIZE - 1)
                pipe.ltrim(QUEUE_KEY, BATCH_SIZE, -1)
                results = await pipe.execute()

            raw_list = results[0]

            if not raw_list:
                await asyncio.sleep(0.05)
                continue

            users = [json.loads(x) for x in raw_list]

            if users:
                async with engine.begin() as conn:
                    stmt = text("""
                                INSERT INTO users (username, email, full_name, password, biography)
                                VALUES (:username, :email, :full_name, :password, :biography) 
                                ON CONFLICT (username) DO NOTHING
                                """)
                    await conn.execute(stmt, users)

                logger.info(f"✅ Saved batch: {len(users)} users")

        except Exception as e:
            logger.error(f"❌ Error: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        print("Stopped")