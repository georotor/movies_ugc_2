# Проектная работа 9 спринта

https://github.com/georotor/ugc_sprint_2

## Выбор хранилища
[Тестирование производительности БД Mongo и Cassandra](https://github.com/georotor/ugc_sprint_2/tree/main/research)


## API
Описание [UGC API](https://github.com/georotor/ugc_sprint_2/tree/main/ugs_api)

API запускается коммандой: `docker-compose up --build`

## Тесты
```
docker-compose -f ugs_api/src/tests/functional/docker-compose.yml up --build
```

## Логирование
```
docker-compose -f elk/docker-compose.yml up
```
