"""Сервис авторизации."""
import logging
from datetime import datetime, timezone
from uuid import UUID

import aiohttp
import backoff
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import decode

from db import redis
from settings import settings

logger = logging.getLogger(__name__)


class JWTBearer(HTTPBearer):
    """Работа с токенами."""

    def __init__(self, auto_error: bool = True):
        """Конструктор класса."""
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> UUID:
        """Работа с credentials.

        Raises:
            HTTPException: HTTP_403_FORBIDDEN

        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if credentials.scheme != 'Bearer':
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail='Invalid authentication scheme.',
                )

            payload = await self.get_payload(credentials.credentials)
            check_auth = await self.check_auth(token=credentials.credentials, payload=payload)
            if not check_auth:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail='Auth: Invalid token or expired token.',
                )

            return payload.get('sub')

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid authorization code.',
        )

    async def get_payload(self, token: str) -> dict:
        """
        Если токен валидный и не истек срок его действия, то возвращает данные токена.

        :param token: Токен для проверки
        :return: Данные из токена в виде словаря

        Raises:
            HTTPException: HTTP_403_FORBIDDEN

        """
        try:
            payload = decode(token, options={'verify_signature': False})
            if payload.get('exp') > datetime.now(timezone.utc).timestamp():
                return payload
        except Exception:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token.')

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Expired token.')

    @backoff.on_exception(backoff.expo, aiohttp.ClientError)
    async def check_auth(self, token: str, payload: dict) -> bool:
        """
        Проверяем валидность в токена во внешнем сервисе и кэшируем результат.

        :param token: Токен
        :param payload: Данные из токена

        """
        if not settings.jwt_validate:
            return True

        cache = await self._jwt_from_cache(payload.get('jti'))
        if cache is not None:
            return bool(int(cache))

        res = False

        session = aiohttp.ClientSession()
        async with session.get(
            settings.auth_url, headers={'Authorization': 'Bearer {0}'.format(token)},
        ) as auth_response:
            if auth_response.status == status.HTTP_200_OK:
                res = True

            await self._put_jwt_to_cache(payload, res)
            return res

    async def _jwt_from_cache(self, jti: UUID) -> bool:
        return await redis.client.get(str(jti))

    async def _put_jwt_to_cache(self, payload: dict, value: bool):
        ex = settings.cache_expire
        dt_now = datetime.now(timezone.utc).timestamp()
        if payload.get('exp') - dt_now < ex:
            ex = payload.get('exp') - datetime.now(timezone.utc).timestamp()

        await redis.client.set(payload.get('jti'), int(value), ex)


bearer = JWTBearer()
