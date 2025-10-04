# Messages API - Backend Assessment (FastAPI + SQLite)

**Author:** Nestor Ortiz

Proyecto de ejemplo para la prueba técnica de backend. Implementa una API que recibe, procesa y almacena mensajes de chat.

## Tecnologías
- Python 3.10+
- FastAPI
- SQLite (por simplicidad)
- SQLAlchemy (ORM)
- Pytest (tests)

## Características incluidas
- Endpoints obligatorios (POST /api/messages, GET /api/messages/{session_id})
- Validación con Pydantic
- Procesamiento de mensajes y metadatos
- Filtro básico de palabras inapropiadas
- Paginación, filtro por remitente y búsqueda por texto
- Manejo de errores con formato definido
- Autenticación simple por API Key (`x-api-key` header)
- WebSocket para notificaciones en tiempo real (`/ws/messages/{session_id}`)
- Rate limiting simple en memoria (requests por IP)
- Dockerfile y docker-compose para despliegue

## Estructura
```
project/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ database.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ repository.py
│  ├─ service.py
│  ├─ auth.py
│  ├─ middleware.py
│  └─ routers/
│     ├─ messages.py
│     └─ ws.py
├─ tests/
│  ├─ test_service.py
│  └─ test_api.py
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ .env.template
└─ README.md
```

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.template .env
# Edita .env y coloca un API_KEY seguro
```

## Ejecutar la app (local)
```bash
uvicorn app.main:app --reload --port 8000
```
Accede a la documentación interactiva en `http://127.0.0.1:8000/docs`

## Docker
```bash
docker build -t messages-api .
docker compose up -d
```

## Endpoints
- `POST /api/messages` : crear/guardar un mensaje (requerido header `x-api-key`)
- `GET  /api/messages/{session_id}` : listar mensajes por sesión (limit, offset, sender, search)
- `WS   /ws/messages/{session_id}` : websocket que envía notificaciones cuando se crea un mensaje

## Tests
```bash
pytest --maxfail=1 -q
```

## Notas
- El filtro de palabras inapropiadas está en `app/service.py` en la variable `FORBIDDEN_WORDS`.
- La autenticación es deliberadamente simple para la evaluación (header `x-api-key`) y está pensada para demostrar la mecánica.
- El rate limiting es una implementación en memoria adecuada para pruebas y desarrollo. En producción usar soluciones como Redis + Limiter.
