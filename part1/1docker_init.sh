#!/bin/bash

docker rm -f lab1 

# запускаем контейнер с постгрес
docker run -d \
  --name lab1 \
  --env POSTGRES_USER=admin \
  --env POSTGRES_PASSWORD=pass \
  --env POSTGRES_DB=db \
  -p 5432:5432 \
  -v "./db_init:/docker-entrypoint-initdb.d" \
  -v ./pgdata:/var/lib/postgresql/data \
  postgres:17

# ждем постгрес
sleep 4

# статус контейнера
docker ps --filter "name=lab1"

# логи
docker logs lab1