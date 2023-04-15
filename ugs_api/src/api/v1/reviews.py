"""Ручка для получения информации об обзорах."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status

from models.aggregate_models import ReviewAggregateBriefModel, ReviewAggregateDetailModel
from services.aggregate_service import AggregateService, get_review_aggregate_service

router = APIRouter()


@router.get(
    '/{review_id}',
    response_model=Optional[ReviewAggregateDetailModel],
    summary='Просмотр обзора',
    description='Подробная информация об обзоре.',
)
async def get_by_id(
    review_id: UUID,
    service: AggregateService = Depends(get_review_aggregate_service),
):
    """Подробная информация об обзоре."""
    review = await service.review.get_by_id(review_id)
    if not review:
        return None

    like = await service.like.get(obj_id=review.obj_id, user_id=review.user_id)
    rating = await service.get_rating(review_id)
    review_data = {
        'review_id': review.review_id,
        'title': review.title,
        'text': review.text,
        'film_score': like.score if like else None,
        'film_id': review.obj_id,
        'user_id': review.user_id,
    }
    review_data.update(rating)
    return ReviewAggregateDetailModel(**review_data)


@router.get(
    '/film/{film_id}',
    response_model=list[ReviewAggregateBriefModel],
    summary='Список обзоров',
    description='Список обзоров для фильма.',
)
async def get_reviews_list(
    film_id: UUID,
    page_size: int = Query(default=10, alias='page[size]', ge=10, le=100),
    page_number: int = Query(default=1, alias='page[number]', ge=1),
    sort: str = Query(default='_id', alias='sort'),
    service: AggregateService = Depends(get_review_aggregate_service),
):
    """Получить список обзоров для конкретного фильма.

    Метод aggregate добавляет дополнительные поля с данными о лайках.
    Сортировку можно изменить на '-avg' (средний бал) или '-sum' (суммарный бал).
    Кроме того, сортировать можно по date, _id или user_id.

    """
    docs = await service.review.aggregate(
        'review_like',
        ['review_id', 'obj_id'],
        'score',
        obj_id=film_id,
        user_id=None,
        page_size=page_size,
        page_number=page_number,
        sort=sort,
    )
    review_data = []
    for doc in docs:
        review_data.append(
            {
                'review_id': doc['review_id'],
                'title': doc['title'],
                'text': doc['text'],
                'film_id': doc['obj_id'],
                'user_id': doc['user_id'],
                'absolute_rating': doc['sum'],
                'average_rating': doc['avg'],
            },
        )
    return [ReviewAggregateBriefModel(**cur_data) for cur_data in review_data]


@router.post(
    '/{review_id}/add_like',
    summary='Добавить лайк',
    description='Добавить лайк иди дизлайк обзору.',
    status_code=status.HTTP_201_CREATED,
)
async def add_like(
    request: Request,
    review_id: UUID,
    score: int = Query(default=10, alias='score', ge=0, le=10),
    service: AggregateService = Depends(get_review_aggregate_service),
):
    """Добавить лайк или дизлайк. Оценки взаимно заменяемы."""
    await service.like.create(
        obj_id=review_id,
        user_id=request.state.user_id,
        score=score,
    )
    return {'status': 'successfully created'}


@router.delete(
    '/{review_id}/remove_like',
    summary='Удалить лайк',
    description='Удалить лайк или дизлайк обзору.',
    status_code=status.HTTP_200_OK,
)
async def delete_like(
    request: Request,
    review_id: UUID,
    service: AggregateService = Depends(get_review_aggregate_service),
):
    """Удалить лайки или дизлайк."""
    await service.like.delete(
        obj_id=review_id,
        user_id=request.state.user_id,
    )
    return {'status': 'successfully deleted'}
