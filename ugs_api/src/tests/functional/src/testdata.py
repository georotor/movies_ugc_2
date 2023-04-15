"""Данные для тестов."""
from datetime import datetime
from uuid import uuid4

import jwt

TEST_USER_ID = str(uuid4())
TEST_FILM_ID = str(uuid4())
TEST_AUTH_TOKEN = jwt.encode(
    {'sub': TEST_USER_ID, 'exp': int(datetime.now().timestamp() + 1000)},
    'secret',
    algorithm='HS256',
)
WRONG_AUTH_TOKEN = jwt.encode(
    {'sub': TEST_USER_ID, 'exp': int(datetime.now().timestamp() - 1)},
    'secret',
    algorithm='HS256',
)
