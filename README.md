### Проект последнего курса (планировщик задач)

#### Stack: Django, Python3.10, PostgreSQL

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
```
### step 3: Launch project
```sh
docker-compose up --build -d 
```
---
##### project is currently developed, so to be continued...