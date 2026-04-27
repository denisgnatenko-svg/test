# FastAPI Time API

Простой тестовый бэкенд на FastAPI, возвращающий текущее время сервера (UTC).

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Эндпоинты

- `GET /` — health-check
- `GET /time` — текущее время сервера

Пример ответа `GET /time`:

```json
{
  "server_time_utc": "2026-04-27T08:20:00.000000+00:00",
  "unix_seconds": 1777278000,
  "timezone": "UTC"
}
```

