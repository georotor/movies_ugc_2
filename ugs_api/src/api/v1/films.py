"""Ручка для получения информации и фильмах."""
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Query, status

from models.response_models import FilmResponseModel
from services.films import FilmService, get_film_service
from services.like import LikeService, get_like_service
from services.review import ReviewService, get_review_service

router = APIRouter()


@router.get(
    '/{film_id}',
    response_model=FilmResponseModel,
    summary='Информация о фильме',
    description='Подробный данные о фильме.',
)
async def get_films_list(
    film_id: UUID,
    service: FilmService = Depends(get_film_service),
):
    """Получить информацию о фильме."""
    ratings = await service.get_rating(film_id)
    reviews = await service.get_review(film_id)

    film_data = {'film_id': film_id}
    film_data.update(ratings)
    film_data.update(reviews)

    return FilmResponseModel(**film_data)


@router.post(
    '/{film_id}/add_like',
    summary='Информация о фильме',
    description='Подробный данные о фильме.',
    status_code=status.HTTP_201_CREATED,
)
async def add_like(
    request: Request,
    film_id: UUID,
    score: int = Query(default=10, alias='score', ge=0, le=10),
    service: LikeService = Depends(get_like_service),
):
    """Добавить лайк или дизлайк. Оценки взаимно заменяемы."""
    await service.create(
        obj_id=film_id,
        user_id=request.state.user_id,
        score=score,
    )


@router.delete(
    '/{film_id}/remove_like',
    summary='Информация о фильме',
    description='Подробный данные о фильме.',
    status_code=status.HTTP_201_CREATED,
)
async def delete_like(
    request: Request,
    film_id: UUID,
    service: LikeService = Depends(get_like_service),
):
    """Удалить лайки или дизлайк."""
    await service.delete(
        obj_id=film_id,
        user_id=request.state.user_id,
    )


@router.post(
    '/{film_id}/create_review',
    summary='Информация о фильме',
    description='Подробный данные о фильме.',
)
async def create_review(
    request: Request,
    film_id: UUID,
    title: str = Query(alias='title'),
    text: str = Query(alias='text'),
    service: ReviewService = Depends(get_review_service),
):

    await service.create(
        obj_id=film_id,
        user_id=request.state.user_id,
        title=title,
        text=text,
    )
