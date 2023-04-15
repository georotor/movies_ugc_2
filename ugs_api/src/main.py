"""Приложение FastAPI."""
import backoff
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis import asyncio as aioredis

from api.v1 import films, reviews, users
from db import redis
from db.mongo import get_mongo
from settings import settings


MAX_CONNECTIONS = 20

mongo = get_mongo()

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
@backoff.on_exception(backoff.expo, (ConnectionError,))
async def startup():
    """Поднимаем Redis при закуске API."""
    if settings.jwt_validate:
        redis.client = await aioredis.from_url(
            'redis://{redis_host}:{redis_port}'.format(
                redis_host=settings.redis_host, redis_port=settings.redis_port,
            ),
            encoding='utf8',
            decode_responses=True,
            max_connections=MAX_CONNECTIONS,
        )

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(reviews.router, prefix='/api/v1/reviews', tags=['reviews'])
app.include_router(users.router, prefix='/api/v1/users', tags=['users'])


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=int('8000'), reload=True)
