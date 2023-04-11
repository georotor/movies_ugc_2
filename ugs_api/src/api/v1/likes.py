"""Ручка для получения информации и лайках."""
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request

from models.ugc_models import Like
from services.like import LikeService, get_like_service

router = APIRouter()


@router.get(
    '/',
    response_model=list[Like],
    summary='Список лайков',
    description='Список всех лайков',
)
async def get_all_likes_list(
    page_size: int = Query(default=10, alias='page[size]', ge=10, le=100),
    page_number: int = Query(default=1, alias='page[number]', ge=1),
    sort: str = Query(default='_id', alias='sort'),
    like_service: LikeService = Depends(get_like_service),
):
    """Получить полный список всех лайков."""
    return await like_service.search(
        film_id=None,
        user_id=None,
        page_size=page_size,
        page_number=page_number,
        sort=sort,
    )


@router.get(
    '/{film_id}',
    response_model=Like,
    summary='Список лайков',
    description='Список лайков для фильма.',
)
async def get_likes_list(
    film_id: UUID,
    page_size: int = Query(default=10, alias='page[size]', ge=10, le=100),
    page_number: int = Query(default=1, alias='page[number]', ge=1),
    sort: str = Query(default='_id', alias='sort'),
    like_service: LikeService = Depends(get_like_service),
):
    """Получить список лайков для конкретного фильма."""
    return await like_service.search(
        film_id=film_id,
        user_id=None,
        page_size=page_size,
        page_number=page_number,
        sort=sort,
    )


@router.post(
    '/add_like/{film_id}',
    summary='Поставить лайк',
    description='Поставить лайк фильму.',
)
async def create_like(
    request: Request,
    film_id: UUID,
    score: int = Query(default=10, alias='score', ge=0, le=10),
    like_service: LikeService = Depends(get_like_service),
):
    """Текущий пользователь ставит лайк фильму."""
    await like_service.create(
        film_id=film_id,
        user_id=request.state.user_id,
        score=score,
    )
    return []
