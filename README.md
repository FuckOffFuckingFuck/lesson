# MyProj

Build docker-compose:
```sh
$ docker compose up -d --build
$ docker compose exec web alembic upgrade head
```

<!-- [Check it](http://localhost:8000/docs) -->


# local run

Запуск локально:
```sh
$ python -m src.main
```

запуск redis без docker-compose:
```sh
$ docker run --name redis -d -p 6379:6379 redis
```

Проверка Redis:
```sh
$ PING
```

Зайти в Redis в Docker:
```sh
$ docker exec -it some_redis_name bash
$ redis-cli
```

del Redis DataBase:
```sh
$ FLUSHDB
```

# async alembic

```sh
$ alembic init -t async alembic
$ alembic revision --autogenerate -m "Some msg"
$ alembic upgrade head
```

## если проблемс с alembic и postgres, то проверить разрешение порта в брандмауэре:

cmd: 
```sh
$ netsh advfirewall firewall add rule name="Postgre Port" dir=in action=allow protocol=TCP localport=5432
```
Где rule name – имя правила, Localport – разрешенный порт


PowerShell:
```sh
$ New-NetFirewallRule -Name 'POSTGRESQL-In-TCP' -DisplayName 'PostgreSQL (TCP-In)' -Direction Inbound -Enabled True -Protocol TCP -LocalPort 5432
```


## Возможные ошибки: 

alembic ищет адрес не локально а так, как он указан внутри контейнера (при создании ревизии "alembic revision --autogenerate"):
```sh
socket.gaierror: [Errno 11001] getaddrinfo failed
```
### Решение:
указать локальный порт вручную: (на месте localhost был db)
"postgresql+asyncpg://postgres:postgres@<ins>localhost</ins>:5432/pg_database"
после этого не забыть вернуть адрес из src.config.settings.DATABASE_URL

### хз поч:
```sh
ModuleNotFoundError: No module named 'src'
```