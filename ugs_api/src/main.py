"""Приложение FastAPI.

Для удобства дебага можно добавить:

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=settings, reload=True)

"""
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from api.v1 import films, likes, reviews
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

app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(reviews.router, prefix='/api/v1/reviews', tags=['reviews'])
