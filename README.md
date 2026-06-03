# Workshop Booking System

Система управления бронированием мастер-классов на Django и Django REST Framework. 
Домашнее задание №1 Серверные фреймворки бэкенд-разработки

## Возможности

- регистрация пользователей;
- авторизация через Basic Auth или сессию DRF;
- просмотр списка мастер-классов;
- создание и просмотр бронирований;
- CRUD мастер-классов для пользователя с ролью администратора;
- запрет повторного бронирования одного мастер-класса одним пользователем.

## Технологии

- Python 3.12;
- Django;
- Django REST Framework;
- SQLite;
- Docker;
- Postman для проверки API.

## Запуск через Docker

```bash
docker compose up --build
```

Приложение будет доступно по адресу `http://localhost:8000/`.

## Локальный запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API

- `POST /api/auth/register/` — регистрация пользователя;
- `GET /api/auth/me/` — данные текущего пользователя;
- `GET /api/workshops/` — список мастер-классов;
- `GET /api/workshops/{id}/` — детали мастер-класса;
- `POST /api/workshops/` — создание мастер-класса для администратора;
- `PUT/PATCH/DELETE /api/workshops/{id}/` — управление мастер-классом для администратора;
- `GET /api/bookings/` — список своих бронирований;
- `POST /api/bookings/` — создание бронирования;
- `GET/PUT/PATCH/DELETE /api/bookings/{id}/` — управление своим бронированием.

Для роли администратора установите пользователю `role=admin` через Django admin или shell.

## Структура

- `accounts` — пользователи и роли;
- `workshops` — мастер-классы;
- `bookings` — бронирования;
- `config` — настройки проекта;
- `postman` — коллекция для проверки API;
- `docs` — дополнительная документация.

# Проверка API через Postman

## Подготовка

1. Запустите проект:

```bash
docker compose up --build
```

или локально:

```bash
python manage.py migrate
python manage.py runserver
```

2. Импортируйте коллекцию:

```text
postman/workshop-booking-system.postman_collection.json
```

3. Проверьте переменную `base_url`. По умолчанию:

```text
http://localhost:8000
```

## Пользователи

Коллекция использует Basic Auth. Обычного пользователя можно создать запросом
`Auth / Register user`.

Если нужен доступ в Django admin, создайте суперпользователя:

```
python manage.py createsuperuser
```

## Рекомендуемый порядок запросов

1. `Auth / Register user`
2. `Auth / Current user`
3. `Workshops / List workshops`
4. `Workshops / Create workshop as admin`
5. `Workshops / Get workshop by id`
6. `Workshops / Update workshop as admin`
7. `Bookings / Create booking`
8. `Bookings / List own bookings`
9. `Bookings / Get booking by id`
10. `Bookings / Delete booking`

После создания мастер-класса коллекция сохраняет `workshop_id`.
После создания бронирования коллекция сохраняет `booking_id`.
