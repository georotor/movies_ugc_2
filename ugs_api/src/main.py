"""Приложение FastAPI."""
from uuid import uuid4

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from api.v1 import films, reviews, users
from db.mongo import get_mongo
from settings import settings

mongo = get_mongo()

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.middleware('http')
async def authenticate_user(request: Request, call_next):
    """Заглушка, в будущем будет обращение к серверу авторизации.

    Решение уже написано в прошлом спринте. Сейчас вместо нормального user_id
    подставляем фейковый UUID.

    Args:
        request: объект Request;
        call_next: колбэк.

    Returns:
        response

    """
    request.state.user_id = uuid4()
    return await call_next(request)

app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(reviews.router, prefix='/api/v1/reviews', tags=['reviews'])
app.include_router(users.router, prefix='/api/v1/users', tags=['users'])


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=int('8000'), reload=True)
