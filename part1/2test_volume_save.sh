#!/bin/bash

echo "1. добавляем новую запись в контейнер lab1"
docker exec -i lab1 psql -U admin -d db -c "INSERT INTO users (username, role) VALUES ('user_test1', 'tester1') ON CONFLICT (username) DO NOTHING;"

echo "2. удаляем контейнер lab1"
docker rm -f lab1

echo "3. запускаем контейнер заново"
./1docker_init.sh

echo "4. проверяем, что запись сохранилась в новом контейнере:"
docker exec -i lab1 psql -U admin -d db -c "SELECT * FROM users;"