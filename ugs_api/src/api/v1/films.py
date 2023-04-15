"""Ручка для получения информации и фильмах."""
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status

from models.aggregate_models import FilmAggregateModel
from services.aggregate_service import AggregateService, get_film_aggregate_service

router = APIRouter()


@router.get(
    '/{film_id}',
    response_model=FilmAggregateModel,
    summary='Информация о фильме',
    description='Подробные данные о фильме.',
)
async def get_film(
    request: Request,
    film_id: UUID,
    service: AggregateService = Depends(get_film_aggregate_service),
):
    """Получить информацию о фильме."""
    ratings = await service.get_rating(film_id)
    reviews = await service.review.search(film_id, sort='-date', page_size=10)
    bookmark = await service.bookmark.get(film_id, request.state.user_id)

    film_data = {
        'film_id': film_id,
        'recent_reviews': reviews,
        'bookmark': bookmark,
    }
    film_data.update(ratings)

    return FilmAggregateModel(**film_data)


@router.post(
    '/{film_id}/add_like',
    summary='Добавить лайк',
    description='Добавить лайк иди дизлайк фильму.',
    status_code=status.HTTP_201_CREATED,
)
async def add_like(
    request: Request,
    film_id: UUID,
    score: int = Query(default=10, alias='score', ge=0, le=10),
    service: AggregateService = Depends(get_film_aggregate_service),
):
    """Добавить лайк или дизлайк. Оценки взаимно заменяемы."""
    await service.like.create(
        obj_id=film_id,
        user_id=request.state.user_id,
        score=score,
    )
    return {'status': 'successfully created'}


@router.delete(
    '/{film_id}/remove_like',
    summary='Удалить лайк',
    description='Удалить лайк иди дизлайк фильму.',
    status_code=status.HTTP_200_OK,
)
async def delete_like(
    request: Request,
    film_id: UUID,
    service: AggregateService = Depends(get_film_aggregate_service),
):
    """Удалить лайки или дизлайк."""
    await service.like.delete(
        obj_id=film_id,
        user_id=request.state.user_id,
    )
    return {'status': 'successfully deleted'}


@router.post(
    '/{film_id}/add_review',
    summary='Добавить обзор',
    description='Добавить обзор к фильму.',
    status_code=status.HTTP_201_CREATED,
)
async def add_review(
    request: Request,
    film_id: UUID,
    title: str = Query(default=..., alias='title'),
    text: str = Query(default=..., alias='text'),
    service: AggregateService = Depends(get_film_aggregate_service),
):
    """Добавить обзор."""
    await service.review.create(
        obj_id=film_id,
        user_id=request.state.user_id,
        title=title,
        text=text,
    )
    return {'status': 'successfully created'}


@router.delete(
    '/{film_id}/remove_review',
    summary='Удалить обзор',
    description='Удалить обзор к фильму.',
    status_code=status.HTTP_200_OK,
)
async def delete_review(
    request: Request,
    film_id: UUID,
    service: AggregateService = Depends(get_film_aggregate_service),
):
    """Удалить обзор."""
    await service.review.delete(
        obj_id=film_id,
        user_id=request.state.user_id,
    )
    return {'status': 'successfully deleted'}
