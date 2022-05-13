# API проекта YaTube

- OpenAPI к блогам проекта YaTube. 
- Для авторизации используются JWT токены.


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

###Примеры запросов к API.