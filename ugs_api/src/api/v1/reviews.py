from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models import Review
from services.review import get_review_service, ReviewService
from uuid import UUID
from typing import Optional

router = APIRouter()


@router.get(
    "/",
    response_model=list[Review],
    summary='Список обзоров',
    description="Список всех обзоров"
)
async def get_all_reviews_list(
    page_size: int = Query(default=10, alias="page[size]", ge=10, le=100),
    page_number: int = Query(default=1, alias="page[number]", ge=1),
    sort: str = Query(default='_id', alias="sort"),
    review_service: ReviewService = Depends(get_review_service),
):
    """Получить полный список всех лайков. """
    return await review_service.search(
        film_id=None,
        user_id=None,
        page_size=page_size,
        page_number=page_number,
        sort=sort
    )


@router.get(
    "/{film_id}",
    response_model=list[Review],
    summary='Список лайков',
    description="Список лайков для фильма."
)
async def get_reviews_list(
    film_id: UUID,
    page_size: int = Query(default=10, alias="page[size]", ge=10, le=100),
    page_number: int = Query(default=1, alias="page[number]", ge=1),
    sort: str = Query(default='_id', alias="sort"),
    review_service: ReviewService = Depends(get_review_service),
):
    """Получить список лайков для конкретного фильма. """
    return await review_service.search(
        film_id=film_id,
        user_id=None,
        page_size=page_size,
        page_number=page_number,
        sort=sort
    )


@router.post(
    "/add_review/{film_id}",
    summary='Написать обзор',
    description="Написать обзор на фильм."
)
async def create_reviews(
    request: Request,
    film_id: UUID,
    title: str = Query(default=..., min_length=3),
    text: str = Query(default=..., min_length=5),
    review_service: ReviewService = Depends(get_review_service),
):
    """Текущий пользователь добавляет обзор на фильм. """
    await review_service.create(
        film_id=film_id,
        user_id=request.state.user_id,
        title=title,
        text=text,
    )
    return []

