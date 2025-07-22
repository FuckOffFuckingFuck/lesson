# MyProj

Build docker-compose
```sh
$ docker compose up -d --build
$ docker compose exec web alembic upgrade head
```

<!-- [Check it](http://localhost:8000/docs) -->

Зайти в Redis в Docker
```sh
$ docker exec -it some_RedisName bash
$ redis-cli
```

Проверка Redis
```sh
$ PING
```
del Redis DataBase
```sh
$ FLUSHDB
```

запуск redis без docker-compose
```sh
$ docker run --name redis -d -p 6379:6379 redis
```

# local run

```sh
$ python -m src.main
```
