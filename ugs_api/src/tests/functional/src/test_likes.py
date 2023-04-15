"""Тесты работы лайков."""
from http import HTTPStatus

import pytest
from testdata import TEST_AUTH_TOKEN, TEST_FILM_ID, TEST_USER_ID

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'score, likes, dislikes', [(0, 0, 1), (5, 0, 0), (10, 1, 0)],
)
async def test_add_like(make_json_request, score, likes, dislikes):
    """Тестируем добавление лайка к фильму.

    Лайк добавляется в ручке фильма. Отображается в личном кабинете
    и в информации о фильме. Пользователь может поставить фильму только один
    лайк / дизлайк. При повторно попытки оценить фильм старое значение должно
    заменяться новым.

    Лайками считаются оценки со значением 10, дизлайками - со значением 0.

    """
    # Добавляем новый лайк
    url = '/api/v1/films/{0}/add_like/'.format(TEST_FILM_ID)
    params = {'score': score}
    response = await make_json_request(url=url, params=params, auth_token=TEST_AUTH_TOKEN)
    assert response.status == HTTPStatus.CREATED

    # Ищем лайк в личном кабинете
    url = '/api/v1/users/my_account'
    response = await make_json_request(
        url=url, auth_token=TEST_AUTH_TOKEN, method='GET',
    )

    users_id_list = [like['user_id'] for like in response.body['recent_likes']]
    films_id_list = [like['obj_id'] for like in response.body['recent_likes']]

    assert TEST_USER_ID in users_id_list
    assert TEST_FILM_ID in films_id_list

    # Ищем закладку в информации о фильме
    url = '/api/v1/films/{0}'.format(TEST_FILM_ID)
    response = await make_json_request(
        url=url, auth_token=TEST_AUTH_TOKEN, method='GET',
    )

    users_id_list = [like['user_id'] for like in response.body['recent_likes']]
    films_id_list = [like['obj_id'] for like in response.body['recent_likes']]

    assert TEST_USER_ID in users_id_list
    assert TEST_FILM_ID in films_id_list

    # Проверяем, что кол-во закладок и значения рейтинга
    assert response.body['likes'] == likes
    assert response.body['dislikes'] == dislikes
    assert response.body['absolute_rating'] == score
    assert response.body['average_rating'] == score


async def test_delete_like(make_json_request):
    """Тестируем добавление лайка к фильму.

    Лайк удаляется в ручке фильма. Отображается в личном кабинете
    и в информации о фильме. Пользователь может поставить фильму только один
    лайк / дизлайк. При повторно попытки оценить фильм старое значение должно
    заменяться новым.

    """
    # Добавляем новый лайк
    url = '/api/v1/films/{0}/remove_like/'.format(TEST_FILM_ID)
    response = await make_json_request(
        url=url, method='DELETE', auth_token=TEST_AUTH_TOKEN,
    )
    assert response.status == HTTPStatus.OK

    # Ищем лайк в личном кабинете
    url = '/api/v1/users/my_account'
    response = await make_json_request(
        url=url, auth_token=TEST_AUTH_TOKEN, method='GET',
    )

    users_id_list = [like['user_id'] for like in response.body['recent_likes']]
    films_id_list = [like['obj_id'] for like in response.body['recent_likes']]

    assert TEST_USER_ID not in users_id_list
    assert TEST_FILM_ID not in films_id_list

    # Ищем закладку в информации о фильме
    url = '/api/v1/films/{0}'.format(TEST_FILM_ID)
    response = await make_json_request(
        url=url, auth_token=TEST_AUTH_TOKEN, method='GET',
    )

    users_id_list = [like['user_id'] for like in response.body['recent_likes']]
    films_id_list = [like['obj_id'] for like in response.body['recent_likes']]

    assert TEST_USER_ID not in users_id_list
    assert TEST_FILM_ID not in films_id_list

    # Проверяем, что кол-во закладок и значения рейтинга
    assert response.body['likes'] == 0
    assert response.body['dislikes'] == 0
    assert response.body['absolute_rating'] is None
    assert response.body['average_rating'] is None
