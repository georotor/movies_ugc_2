"""Тесты работы закладок."""
from http import HTTPStatus

import pytest
from testdata import TEST_AUTH_TOKEN, TEST_FILM_ID, TEST_USER_ID

pytestmark = pytest.mark.asyncio


async def test_add_bookmark(make_json_request):
    """Тестируем добавление закладки.

    Закладка добавляется в ручке пользователя. Отображается в личном кабинете
    и в информации о фильме.

    """
    # Создаем новую закладку
    url = '/api/v1/users/bookmarks/add/{0}/'.format(TEST_FILM_ID)
    response = await make_json_request(url=url, auth_token=TEST_AUTH_TOKEN)
    assert response.status == HTTPStatus.CREATED

    # Ищем закладку в личном кабинете
    url = '/api/v1/users/my_account'
    response = await make_json_request(
        url=url, auth_token=TEST_AUTH_TOKEN, method='GET',
    )

    users_id_list = [b_mark['user_id'] for b_mark in response.body['bookmarks']]
    films_id_list = [b_mark['obj_id'] for b_mark in response.body['bookmarks']]

    assert TEST_USER_ID in users_id_list
    assert TEST_FILM_ID in films_id_list

    # Ищем закладку в информации о фильме
    url = '/api/v1/films/{0}'.format(TEST_FILM_ID)
    response = await make_json_request(
        url=url, auth_token=TEST_AUTH_TOKEN, method='GET',
    )

    assert response.body['bookmark']['user_id'] == TEST_USER_ID
    assert response.body['bookmark']['obj_id'] == TEST_FILM_ID


async def test_delete_bookmark(make_json_request):
    """Тестируем удаление закладки.

    Закладка добавляется в ручке пользователя. Отображается в личном кабинете
    и в информации о фильме.

    """
    # Удаляем созданную ранее закладку
    url = '/api/v1/users/bookmarks/remove/{0}/'.format(TEST_FILM_ID)
    response = await make_json_request(
        url=url, auth_token=TEST_AUTH_TOKEN, method='DELETE',
    )
    assert response.status == HTTPStatus.OK

    # Ищем закладку в личном кабинете
    url = '/api/v1/users/my_account'
    response = await make_json_request(
        url=url, auth_token=TEST_AUTH_TOKEN, method='GET',
    )

    users_id_list = [b_mark['user_id'] for b_mark in response.body['bookmarks']]
    films_id_list = [b_mark['obj_id'] for b_mark in response.body['bookmarks']]

    assert TEST_USER_ID not in users_id_list
    assert TEST_FILM_ID not in films_id_list

    # Ищем закладку в информации о фильме
    url = '/api/v1/films/{0}'.format(TEST_FILM_ID)
    response = await make_json_request(
        url=url, auth_token=TEST_AUTH_TOKEN, method='GET',
    )

    assert not response.body['bookmark']
    assert not response.body['bookmark']
