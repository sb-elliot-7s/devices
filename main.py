import aioredis
from aioredis import Redis
from fastapi import FastAPI, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from configs import configs
from db import get_session
from repositories import Repository
from schemas import AnagramSchema, AnagramResponseSchema, DeviceSchema

app = FastAPI()

IS_ANAGRAM_COUNT = 'is_anagram_count'


@app.post('/anagrams')
async def check_anagram(strings: AnagramSchema):
    redis: Redis = await aioredis.from_url(configs.redis_host)
    if is_anagram := sorted(strings.first_string) == sorted(strings.second_string):
        await redis.incr(name=IS_ANAGRAM_COUNT)
    count = await redis.get(name=IS_ANAGRAM_COUNT) or 0
    return AnagramResponseSchema(is_anagram=is_anagram, count=count)


# @app.delete('/anagrams', status_code=status.HTTP_204_NO_CONTENT)
# async def remove_cache():
#     redis: Redis = await aioredis.from_url(configs.redis_host)
#     await redis.flushall()


@app.post('/', status_code=status.HTTP_201_CREATED)
async def create_device(session: AsyncSession = Depends(get_session)):
    await Repository(session=session).save_devices()


@app.get('/', status_code=status.HTTP_200_OK, response_model=list[DeviceSchema])
async def devices(session: AsyncSession = Depends(get_session)):
    return await Repository(session=session).get_devices()
