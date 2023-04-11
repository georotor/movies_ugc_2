"""Ручка для получения информации и фильмах."""
from uuid import UUID

from fastapi import APIRouter, Depends

from models.ugc_models import FilmViewModel
from services.films import FilmService, get_film_service

router = APIRouter()


@router.get(
    '/{film_id}',
    response_model=FilmViewModel,
    summary='Информация о фильме',
    description='Подробный данные о фильме.',
)
async def get_likes_list(
    film_id: UUID,
    film_service: FilmService = Depends(get_film_service),
):
    """Получить информацию о фильме."""
    film_data = {'film_id': film_id}
    ratings = await film_service.get_rating(film_id)
    reviews = await film_service.get_review(film_id)
    film_data.update(ratings)
    film_data.update(reviews)
    return FilmViewModel(**film_data)
