"""Тесты работы сервиса авторизации."""
from http import HTTPStatus
from uuid import uuid4

import pytest
from testdata import TEST_AUTH_TOKEN, WRONG_AUTH_TOKEN

pytestmark = pytest.mark.asyncio


AUTH_ENDPOINTS = (
    '/api/v1/users/my_account',
    '/api/v1/films/{0}'.format(uuid4()),
)

NO_AUTH_ENDPOINTS = (
    '/api/v1/users/{}/'.format(uuid4()),
    '/api/v1/reviews/{0}'.format(uuid4()),
)


@pytest.mark.parametrize('url', AUTH_ENDPOINTS)
async def test_endpoints_with_auth_positive(make_json_request, url):
    response = await make_json_request(
        url=url, auth_token=TEST_AUTH_TOKEN, method='GET',
    )
    assert response.status == HTTPStatus.OK


@pytest.mark.parametrize('url', AUTH_ENDPOINTS)
async def test_endpoints_with_auth_no_token(make_json_request, url):
    response = await make_json_request(
        url=url, auth_token=None, method='GET',
    )
    assert response.status == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize('url', AUTH_ENDPOINTS)
async def test_endpoints_with_auth_wrong_token(make_json_request, url):
    response = await make_json_request(
        url=url, auth_token=WRONG_AUTH_TOKEN, method='GET',
    )
    assert response.status == HTTPStatus.FORBIDDEN


@pytest.mark.parametrize('url', NO_AUTH_ENDPOINTS)
async def test_endpoints_with_no_auth(make_json_request, url):
    response = await make_json_request(
        url=url, method='GET',
    )
    assert response.status == HTTPStatus.OK
