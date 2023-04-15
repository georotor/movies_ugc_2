"""Ручка для получения информации и фильмах."""
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status

from models.aggregate_models import UserResponseModel
from services.aggregate_service import (AggregateService,
                                        get_user_aggregate_service)

router = APIRouter()


@router.get(
    '/my_account',
    response_model=UserResponseModel,
    summary='Личный кабинет',
    description='Подробная информация о своей активности.',
)
async def user_detail(
    request: Request,
    service: AggregateService = Depends(get_user_aggregate_service),
):
    """Личный кабинет пользователя с полной информацией."""
    user_id = request.state.user_id
    likes = await service.like.search(user_id=user_id, sort='-date', page_size=10)
    reviews = await service.review.search(user_id=user_id, sort='-date', page_size=10)
    bookmarks = await service.bookmark.search(user_id=user_id, sort='-date', page_size=10)

    user_data = {
        'user_id': user_id,
        'recent_likes': likes,
        'recent_reviews': reviews,
        'bookmarks': bookmarks,
    }

    return UserResponseModel(**user_data)


@router.get(
    '/{user_id}',
    summary='Информация о пользователе',
    description='Минимальная информация о любом пользователе.',
    status_code=status.HTTP_201_CREATED,
)
async def get_user(
    request: Request,
    service: AggregateService = Depends(get_user_aggregate_service),
):
    """Просмотр минимальной информации о любом пользователе."""
    user_id = request.state.user_id
    reviews = await service.review.search(user_id, sort='-date', page_size=10)

    user_data = {
        'user_id': user_id,
        'recent_reviews': reviews,
    }

    return UserResponseModel(**user_data)


@router.post(
    '/bookmarks/add/{film_id}',
    summary='Добавить закладку',
    description='Добавить закладку для фильма.',
    status_code=status.HTTP_201_CREATED,
)
async def add_bookmark(
    request: Request,
    film_id: UUID,
    timestamp: int = Query(default=0, alias='timestamp'),
    service: AggregateService = Depends(get_user_aggregate_service),
):
    """Добавить закладку для фильма."""
    await service.bookmark.create(
        obj_id=film_id,
        user_id=request.state.user_id,
        timestamp=timestamp,
    )
    return {'status': 'successfully created'}


@router.delete(
    '/bookmarks/remove/{film_id}',
    summary='Удалить закладку',
    description='Удалить закладку для фильма.',
    status_code=status.HTTP_200_OK,
)
async def remove_bookmark(
    request: Request,
    film_id: UUID,
    service: AggregateService = Depends(get_user_aggregate_service),
):
    """Удалить закладку для фильма."""
    await service.bookmark.delete(
        obj_id=film_id,
        user_id=request.state.user_id,
    )
    return {'status': 'successfully deleted'}
