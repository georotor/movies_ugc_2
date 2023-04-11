from logging import config as logging_config
from uuid import UUID, uuid4

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from api.v1 import likes, films, reviews
from settings import settings
from db.mongo import get_mongo

mongo = get_mongo()

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.middleware('http')
async def authenticate_user(request: Request, call_next):
    """Заглушка, в будущем будет обращение к серверу авторизации
    (решение уже написано в прошлом спринте). Сейчас вместо нормального user_id
    подставляем фейковый UUID.

    """
    request.state.user_id = uuid4()
    response = await call_next(request)
    return response

app.include_router(likes.router, prefix="/api/v1/likes", tags=["likes"])
app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["reviews"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
