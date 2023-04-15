"""Отправка информации в анализатор UGC_1 API."""
import json
from functools import lru_cache
import backoff

import aiohttp
from fastapi import Request

from core.logger import logger
from settings import settings

API_URL = settings.logger_api_url


class LogsSender:
    """Отправка информации в анализатор UGC_1 API."""

    @backoff.on_exception(backoff.expo, aiohttp.ClientError)
    async def send_bookmarks_logs(self, request: Request, bookmark_data):
        """Отправка информации о новой закладке."""
        session = aiohttp.ClientSession()
        async with session.post(
            '{0}/film/views'.format(API_URL),
            data=json.dumps(bookmark_data),
            headers=request.headers,
        ) as resp:
            logger.debug('Отправлены данные в UGC_1 API: {0}'.format(resp.status))


@lru_cache()
def get_logs_sender():
    """DI для FastAPI. Возвращает сервис для работы с обзорами."""
    return LogsSender()
