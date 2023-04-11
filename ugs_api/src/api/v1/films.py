from fastapi import APIRouter, Depends, HTTPException, Query
from models import Like, FilmViewModel
from services.like import get_like_service, LikeService
from services.films import FilmService, get_film_service
from uuid import UUID
from models import FilmViewModel

router = APIRouter()


@router.get(
    "/{film_id}",
    response_model=FilmViewModel,
    summary='Информация о фильме',
    description="Подробный данные о фильме."
)
async def get_likes_list(
    film_id: UUID,
    film_service: FilmService = Depends(get_film_service),
):
    """Получить информацию о фильме. """
    film_data = {'film_id': film_id}
    ratings = await film_service.get_rating(film_id)
    reviews = await film_service.get_review(film_id)
    film_data.update(ratings)
    film_data.update(reviews)
    return FilmViewModel(**film_data)

