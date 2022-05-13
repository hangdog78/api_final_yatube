# API проекта YaTube

- OpenAPI к блогам проекта YaTube. 
- Для авторизации используются JWT токены.
- После старта проекта документация по API доступна по адресу: http://127.0.0.1:8000/redoc/



### Как развернуть проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/hangdog78/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
venv/Scripts/Activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов к API.

>Получение JWT токена:

```
POST запрос:
http://127.0.0.1:8000/api/v1/jwt/create/

Content type: application/json
{
"username": "string",
"password": "string"
}
```

>Получение пагинированного списка постов:

```
GET запрос:
http://127.0.0.1:8000/api/v1/posts/?offset=3&limit=10

Параметры:

offset: выбранная страница,
limit: количество постов на странице

```
>Создание публикации
```
POST запрос:
http://127.0.0.1:8000/api/v1/jwt/create/

Content type: application/json
{
"text": "string",
"image": "string",
"group": 0
}
```