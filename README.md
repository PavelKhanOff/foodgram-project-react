# Foodgram
### Описание
Проект **Foodgram** позволяет постить рецепты, делиться и скачивать списки продуктов
### Алгоритм регистрации пользователей:
Регистрация проходит на сайте, по форме регистрации
### Установка
Проект собран в Docker 20.10.06 и содержит четыре образа:
- backend - образ бэка проекта
- frontend - образ фронта проекта
- postgres - образ базы данных PostgreSQL v 12.04
- nginx - образ web сервера nginx
#### Команда клонирования репозитория:
```bash
git clone https://github.com/PavelKhanOff/foodgram-project-react 
```
#### Запуск проекта:
- [Установите Докер](https://docs.docker.com/engine/install/)
- Выполнить команду: 
```bash
docker pull pavelkhan/foodgram-project-react :latest
```
#### Первоначальная настройка Django:
```bash
- docker-compose exec web python manage.py migrate --noinput
- docker-compose exec web python manage.py collectstatic --no-input
```
#### Создание суперпользователя:
```bash
- docker-compose exec web python manage.py createsuperuser
```
#### Заполнение .env:
Чтобы добавить переменную в .env необходимо открыть файл .env в корневой директории проекта и поместить туда переменную в формате имя_переменной=значение.
Пример .env файла:

DB_ENGINE=my_db
DB_NAME=db_name
POSTGRES_USER=my_user
POSTGRES_PASSWORD=my_pass
DB_HOST=db_host
DB_PORT=db_port

#### Автор:
Автор Павел Хан. Задание было выполнено в рамках курса от Yandex Praktikum бэкенд разработчик.
#### Workflow badge:
https://github.com/pavelkhanoff/foodgram-project-react/actions/workflows/main.yml/badge.svg
#### Server address:
130.193.52.127
#### Superuser pass&email:
email: admin@admin.ru
pass: admin
