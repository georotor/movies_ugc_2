"""Тесты работы обзоров."""
from http import HTTPStatus

import pytest
from testdata import TEST_AUTH_TOKEN, TEST_FILM_ID, TEST_USER_ID

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'title, text, status',
    [
        ('Title_1', 'Some_long_text', HTTPStatus.CREATED),
        ('Title_2', 'X', HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
async def test_add_like(make_json_request, title, text, status):
    """Тестируем добавление обзора.

    Обзор добавляется в ручке фильма. Отображается в личном кабинете
    и в информации о фильме.

    Длинна текста (text) рецензии должна быть не менее 5 символов.

    """
    # Добавляем новый лайк
    url = '/api/v1/films/{0}/add_review/'.format(TEST_FILM_ID)
    params = {'title': title, 'text': text}
    response = await make_json_request(
        url=url, params=params, auth_token=TEST_AUTH_TOKEN,
    )
    assert response.status == status

    # Ищем лайк в личном кабинете
    url = '/api/v1/users/my_account'
    response = await make_json_request(
        url=url, auth_token=TEST_AUTH_TOKEN, method='GET',
    )

    users_id_list = [review['user_id'] for review in response.body['recent_reviews']]
    films_id_list = [review['obj_id'] for review in response.body['recent_reviews']]

    assert TEST_USER_ID in users_id_list
    assert TEST_FILM_ID in films_id_list

    # Ищем закладку в информации о фильме
    url = '/api/v1/films/{0}'.format(TEST_FILM_ID)
    response = await make_json_request(
        url=url, auth_token=TEST_AUTH_TOKEN, method='GET',
    )

    users_id_list = [review['user_id'] for review in response.body['recent_reviews']]
    films_id_list = [review['obj_id'] for review in response.body['recent_reviews']]

    assert TEST_USER_ID in users_id_list
    assert TEST_FILM_ID in films_id_list


async def test_delete_like(make_json_request):
    """Тестируем удаление обзора.

    Обзор удаляется в ручке фильма. Отображается в личном кабинете
    и в информации о фильме.

    """
    # Добавляем новый лайк
    url = '/api/v1/films/{0}/remove_review/'.format(TEST_FILM_ID)
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
