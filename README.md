## MyProj

Build docker-compose
```sh
$ docker compose up -d --build
$ docker compose exec web alembic upgrade head
```

<!-- [Check it](http://localhost:8000/docs) -->


# local run

```sh
$ python -m src.main
```

запуск redis без docker-compose
```sh
$ docker run --name redis -d -p 6379:6379 redis
```

Проверка Redis
```sh
$ PING
```

Зайти в Redis в Docker
```sh
$ docker exec -it some_RedisName bash
$ redis-cli
```

del Redis DataBase
```sh
$ FLUSHDB
```

# если проблемс с алембик и постгрес, то проверить разрешение порта в бранмауэр:

cmd: 
```sh
$ netsh advfirewall firewall add rule name="Postgre Port" dir=in action=allow protocol=TCP localport=5432
```

PowerShell:
```sh
$ New-NetFirewallRule -Name 'POSTGRESQL-In-TCP' -DisplayName 'PostgreSQL (TCP-In)' -Direction Inbound -Enabled True -Protocol TCP -LocalPort 5432
```


# Возможные ошибки: 

Алембик ищет адрес не локально а так, как он указан внутри контейнера (при создании ревизии "alembic revision --autogenerate"):
```sh
$ socket.gaierror: [Errno 11001] getaddrinfo failed
```
Решение:
указать локальный порт вручную: (на месте localhost был db)
"postgresql+asyncpg://postgres:postgres@localhost:5432/pg_database"
после этого не забыть вернуть адрес из src.config.settings.DATABASE_URL

хз поч:
```sh
$ ModuleNotFoundError: No module named 'src'
```