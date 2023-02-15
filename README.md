# ToDoList
### Данный проект представляет собой backend-часть web-приложения планировщика задач.<br> Полную версию можно посмотреть на www.emotzart.ru
<hr>
<center> 

<b>Возможности:</b>
* Создание разных досок с целями <br>
* Создание разных категорий <br>
* Создание целей с дедлайнами <br>
* Шеринг досок между пользователями (с правами читателя\редактора) <br>
* Аутентификация через ВКонтакте <br>

</center>

<hr/>

### Stack: Django, Python3.10, PostgreSQL

## Installation
### step 1: venv, poetry and packages installation
##### 1) create virtual environment
```sh
python3 -m venv venv && source venv/bin/activate
```
##### 2) install poetry
```sh
pip install poetry
```
##### 3) install packages
```sh
poetry install
```

### step 2: Create and configure .env file
##### 1) create .env file in root
```sh
touch .env
```
##### 2) fill .env file like:
```xml
SECRET_KEY='some_secret_key'
DEBUG=True

DB_ENGINE=django.db.backends.postgresql
DB_NAME=todolist
DB_USER=todolist
DB_PASSWORD=todolist
DB_HOST=localhost
DB_PORT=5432

VK_OAUTH2_KEY=your_vk_app_number
VK_OAUTH2_SECRET=your_vk_app_secret_key

BOT_TOKEN=your_telegram_bot_token
```
### step 3: Launch project
```sh
docker-compose up --build -d 
```
---
### Test run:
##### 1) Launch postgres:
```sh
docker-compose up postgres
```
##### 2) Run tests
```sh
pytest
```