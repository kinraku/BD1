## запуск не через compose
docker run -d \
  --name lab1.2 \
  -p 8000:8000 \
  -v "./logs:/work/logs" \
  -v "./config.json:/work/config.json" \
  lab1.2:latest

## удаляем контейнер, смотрим логи 
docker rm -f lab1.2

## подключения
### через контейнер
docker exec -it lab1.2 bash

curl http://localhost:8000/

curl http://localhost:8000/calculate?n=6
### извне
http://localhost:8000
