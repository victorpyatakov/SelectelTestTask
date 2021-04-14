# Тестовое задание Selectel

## Запуск:
* Запустить докер контейнеры приложения и БД PostgreSQL
```shell script
docker-compose up -d  
```
* Открыть терминал и выполнить команду для перевода к командному интерфейсу докер контейнера приложения
```shell script
docker exec -it testtask_flask_1 /bin/sh
```
* Выполнить команду инициализации БД 
```shell script
python manage.py db init
```
* Выполнить миграции
```shell script
python manage.py db migrate
```
* Создать таблицы в БД
```shell script
python manage.py db upgrade
```
* Заполнить таблицы данными
```shell script
python manage.py db_create
```
* Запустить тесты
```shell script
python tests.py
```
## Описание url:
* / - стартовая страница с списком API endpoints
* /api/rooms - api endpint для получения информации о всех комнатах
* /api/rooms/pk - api endpint для получения информации о конкретной комнате
* /api/customers - api endpint для получения информации о всех клиентах
* /api/customers/pk - api endpint для получения информации о конкретном клиенте
* /api/racks - api endpint для получения информации о всех стойках
* /api/racks/pk - api endpint для получения информации о конкретной стойке
* /api/busy_racks - api endpoint для получения списка занятых стоек с именем комнаты и именем клиента
* /api/racks_with_max_size - api endpoint для получения списка всех комнат, с наибольшим размером стойки
* /api/customers_in_rooms - api endpoint для получения списка всех комнат с массивом id клиентов, у которых есть занятые стойки
* /api/sum - api endpoint для получения суммы переданных аргументов
* /api/dif - api endpoint для получения разности переданных аргументов
* /api/prod - api endpoint для получения произведения переданных аргументов
* /api/div - api endpoint для получения частного переданных аргументов

## Работа с API:
### API endpoint: api/rooms
* методы: GET
* JSON:
```shell script
{
    "rooms": [
        {
            "id": 1,
            "name": "Room1"
        },
        ...
        {
            "id": N,
            "name": "RoomN"
        },
}
```
### API endpoint: api/rooms/pk
* методы: GET
* JSON:
```shell script
{
    "id": 1,
    "name": "Room1"
}
```
### API endpoint: api/customers
* методы: GET
* JSON:
```shell script
{
    "rooms": [
        {
            "id": 1,
            "name": "Client-1"
        },
        ...
        {
            "id": N,
            "name": "Client-N"
        },
}
```
### API endpoint: api/customers/pk
* методы: GET
* JSON:
```shell script
{
    "id": 1,
    "name": "Client-1"
}
```
### API endpoint: api/racks
* методы: GET
* JSON:
```shell script
{
    "racks": [
        {
            "customer_id": 1,
            "id": 1,
            "name": "Rack1",
            "room_id": 1,
            "size": 42,
            "state": "occupied"
        },
        ...
        {
            "customer_id": 1,
            "id": N,
            "name": "RackN",
            "room_id": 1,
            "size": 42,
            "state": "occupied"
        },
}
        
```
### API endpoint: api/racks/pk
* методы: GET
* JSON:
```shell script
{
    "customer_id": 1,
    "id": 1,
    "name": "Rack1",
    "room_id": 1,
    "size": 42,
    "state": "occupied"
}
```
### API endpoint: api/busy_racks
* методы: GET
* JSON:
```shell script
{
    "0": {
        "customer_name": "Client-1",
        "rack_id": 1,
        "rack_name": "Rack1",
        "room_name": "Room1"
    },
    "1": {
        "customer_name": "Client-2",
        "rack_id": 2,
        "rack_name": "Rack2",
        "room_name": "Room1"
    },
    ...
}
```  
### API endpoint: api/racks_with_max_size
* методы: GET
* JSON:
```shell script
{
    "0": {
        "rack_id": 6,
        "rack_size": 47,
        "room_id": 3
    },
    "1": {
        "rack_id": 4,
        "rack_size": 42,
        "room_id": 2
    },
    ...
}
```  
### API endpoint: api/customers_in_rooms
* методы: GET
* JSON:
```shell script
{
    "0": {
        "customers_id": [
            1,
            2
        ],
        "room_id": 1,
        "room_name": "Room1"
    },
    "1": {
        "customers_id": [
            1
        ],
        "room_id": 2,
        "room_name": "Room2"
    },
    ...
}
```  
### API endpoint: api/sum
* методы: POST
* JSON request:
```shell script
{
    "args" : [1,2,3,4],
    "last_arg_multiplier" : 2,
    "reverse": "False"
}
``` 
* JSON response:
```shell script
{
    "result": 14
}
``` 
### API endpoint: api/dif
* методы: POST
* JSON request:
```shell script
{
    "args" : [1,2,3,4],
    "last_arg_multiplier" : 2,
    "reverse": "False"
}
``` 
* JSON response:
```shell script
{
    "result": -12
}
``` 
### API endpoint: api/prod
* методы: POST
* JSON request:
```shell script
{
    "args" : [1,2,3,4],
    "last_arg_multiplier" : 2,
    "reverse": "False"
}
``` 
* JSON response:
```shell script
{
    "result": 48
}
``` 
### API endpoint: api/div
* методы: POST
* JSON request:
```shell script
{
    "args" : [1,2,3,4],
    "last_arg_multiplier" : 3,
    "reverse": "True"
}
``` 
* JSON response:
```shell script
{
    "result": 2.0
}
``` 
#### Возможные проблемы:
* Если не выполнилась команда
```shell script
docker exec -it testtask_flask_1 /bin/sh
```
* Необходимо выполнить команду для просмотра активных контейнеров
```shell script
docker ps
```
* Найти CONTAINER ID нашего запущенного приложения и вставить его в команду
```shell script
docker exec -it <CONTAINER ID> /bin/sh
```
