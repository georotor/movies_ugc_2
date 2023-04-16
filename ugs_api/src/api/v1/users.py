"""Ручка для получения информации и фильмах."""
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status

from core.logger import logger
from core.logs_sender import LogsSender, get_logs_sender
from models.aggregate_models import UserResponseModel
from services.aggregate_service import AggregateService, get_user_aggregate_service
from services.auth import bearer

router = APIRouter()


@router.get(
    '/my_account',
    response_model=UserResponseModel,
    summary='Личный кабинет',
    description='Подробная информация о своей активности.',
)
async def user_detail(
    user_id: UUID = Depends(bearer),
    service: AggregateService = Depends(get_user_aggregate_service),
):
    """Личный кабинет пользователя с полной информацией."""
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
)
async def get_user(
    user_id: UUID,
    service: AggregateService = Depends(get_user_aggregate_service),
):
    """Просмотр минимальной информации о любом пользователе."""
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
    user_id: UUID = Depends(bearer),
    service: AggregateService = Depends(get_user_aggregate_service),
    log_sender: LogsSender = Depends(get_logs_sender),
):
    """Добавить закладку для фильма."""
    await service.bookmark.create(
        obj_id=film_id,
        user_id=user_id,
        timestamp=timestamp,
    )
    logger.debug('Добавлена закладка для фильма {0}'.format(film_id))
    await log_sender.send_bookmarks_logs(
        request, {'film_id': film_id, timestamp: timestamp},
    )
    return {'status': 'successfully created'}


@router.delete(
    '/bookmarks/remove/{film_id}',
    summary='Удалить закладку',
    description='Удалить закладку для фильма.',
    status_code=status.HTTP_200_OK,
)
async def remove_bookmark(
    film_id: UUID,
    user_id: UUID = Depends(bearer),
    service: AggregateService = Depends(get_user_aggregate_service),
):
    """Удалить закладку для фильма."""
    await service.bookmark.delete(
        obj_id=film_id,
        user_id=user_id,
    )
    logger.debug('Удаленка закладка для фильма {0}'.format(film_id))
    return {'status': 'successfully deleted'}
