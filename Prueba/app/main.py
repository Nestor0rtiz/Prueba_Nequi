import os
from fastapi import FastAPI
from .routers import messages, ws
from .middleware import RateLimitMiddleware
from .auth import api_key_dependency

app = FastAPI(title='Messages API - Nequi Assessment')

# Middleware: rate limiting
app.add_middleware(RateLimitMiddleware, max_requests=60, window_seconds=60)

# include routers (messages endpoints require api key dependency)
app.include_router(messages.router, dependencies=[api_key_dependency])
app.include_router(ws.router)

@app.get('/', tags=['root'])
def root():
    return {'status': 'ok', 'message': 'Messages API is running'}
