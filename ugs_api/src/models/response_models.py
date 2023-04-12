from uuid import UUID
from models.ugc_models import Like, Review, ORJSONBaseModel
from typing import Optional


class LikesResponseModel(ORJSONBaseModel):
    films: list[Like]
    reviews: list[Like]


class FilmResponseModel(ORJSONBaseModel):
    """Общая информация и фильме: лайки, рейтинг, рецензии и пр."""

    film_id: UUID
    recent_likes: list[Optional[Like]]
    absolute_rating: Optional[int]
    average_rating: Optional[float]
    likes: int
    dislikes: int
    recent_reviews: list[Optional[Review]]
