"""Приложение FastAPI."""
import logging
from logging import config as logging_config


import backoff
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from redis import asyncio as aioredis

from api.v1 import films, reviews, users
from db import redis_db
from db.mongo import get_mongo
from logger import LOGGING
from settings import settings

logging_config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

MAX_CONNECTIONS = 20

mongo = get_mongo()

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.middleware('http')
async def before_request(request: Request, call_next):
    """Проверяем наличие Request-Id."""
    request_id = request.headers.get('X-Request-Id')

    if not request_id:
        logger.warning('X-Request-Id is required')
        raise RuntimeError('X-Request-Id is required')

    custom_logger = logging.LoggerAdapter(
        logger, extra={'tag': 'ugs_api', 'request_id': request_id},
    )
    custom_logger.info('X-Request-Id: {0}'.format(request_id))

    return await call_next(request)


@app.on_event('startup')
@backoff.on_exception(backoff.expo, (ConnectionError,))
async def startup():
    """Поднимаем Redis при закуске API."""
    if settings.jwt_validate:
        redis_db.client = await aioredis.from_url(
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
