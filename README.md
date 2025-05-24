# Контейнеризация распределённого приложения

## Описание проекта

Проект состоит из двух микросервисов:

- Telegram Bot — получает команды пользователя, сохраняет ссылки и отправляет уведомления.
- Scrapper — отслеживает изменения ресурсов, уведомляет бот через HTTP.

Они используют PostgreSQL и общаются по HTTP в одной docker-сети.

## Архитектура

```
Telegram Bot (8080)  ←→  Scrapper (8081)
     |                        |
PostgreSQL (bot)       PostgreSQL (scrapperdb)
```

## Инструкция по запуску

### 1. Клонировать репозиторий

```bash
git clone <ссылка>
cd project-laba
```

### 2. Создать файл .env

Создать файл `.env` в корне проекта и прописать:

```
POSTGRES_USER=admin
POSTGRES_PASSWORD=1357
POSTGRES_DB=postgres

TELEGRAM_BOT_TOKEN=ваш_токен
BOT_SERVER_PORT=8080
SCRAPPER_SERVER_PORT=8081

BOT_DATASOURCE_URL=jdbc:postgresql://postgres:5432/bot
BOT_DATASOURCE_USERNAME=admin
BOT_DATASOURCE_PASSWORD=1357

SCRAPPER_DATASOURCE_URL=jdbc:postgresql://postgres:5432/scrapperdb
SCRAPPER_DATASOURCE_USERNAME=admin
SCRAPPER_DATASOURCE_PASSWORD=qwerty

BOT_NOTIFICATION_URL=http://bot:8080/bot/notify
SCRAPPER_LINK_URL=http://scrapper:8081/scrapper/link
```

### 3. Собрать и запустить

```bash
docker-compose up --build -d
```

### 4. Проверить состояние

```bash
docker-compose ps
docker-compose logs -f bot
docker-compose logs -f scrapper
```

### 5. Проверка базы и сети

```bash
docker exec -it postgres_db psql -U admin -d bot -c "\dt"
docker network inspect app-network
```

## Тестирование

### Автоматические тесты

```bash
pip install -r reqs.txt
pytest tests/
```

Покрытие:

- команды: `/start`, `/track`, `/list`, `/search`
- REST-запрос: `/bot/notify`

### Ручное тестирование

- Отправить команды боту в Telegram
- Зайти на http://localhost:8080/swagger-ui/index.html#/ (если есть)
- Посмотреть логи и работу scrapper

## Структура проекта

```
├── main.py
├── handler.py
├── database.py
├── reqs.txt
├── .env
├── tests/
│   ├── test_bot.py
│   └── test_rest_notify.py
├── postgres-init/
│   └── 01-create-databases.sql
├── docker-compose.yml
├── bot/
│   └── Dockerfile
├── scrapper/
│   └── Dockerfile
```