# Movies: Сервис пользовательских данных

[![CI](https://github.com/georotor/movies_ugc_2/actions/workflows/check.yml/badge.svg)](https://github.com/georotor/movies_ugc_2/actions/workflows/check.yml)
[![CI](https://github.com/georotor/movies_ugc_2/actions/workflows/tests.yml/badge.svg)](https://github.com/georotor/movies_ugc_2/actions/workflows/tests.yml)

## Архитектура

![Архитектура](https://github.com/georotor/movies_ugc_2/blob/main/docs/schema.png?raw=true)

## Компоненты
- [FastAPI - реализация API](https://github.com/georotor/movies_ugc_2/tree/main/ugs_api)
- Mongo - хранилище
- Redis - хранилище для кэша
- [ELK - хранение и обработка логов](https://github.com/georotor/movies_ugc_2/tree/main/elk)

## Выбор хранилища
[Тестирование производительности БД Mongo и Cassandra](https://github.com/georotor/movies_ugc_2/tree/main/research)

## Документация
- [Общее описание API](https://github.com/georotor/movies_ugc_2/tree/main/ugs_api)
- Swagger API доступен после запуска по адресу http://127.0.0.1/api/openapi

## Запуск сервиса

```commandline
docker-compose up --build
```

## Тесты
```
docker-compose -f ugs_api/src/tests/functional/docker-compose.yml up --build
```

## Логирование
```
docker-compose -f elk/docker-compose.yml up
```
