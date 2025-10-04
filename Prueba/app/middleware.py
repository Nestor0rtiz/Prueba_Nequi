import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        # store: {ip: [timestamps]}
        self.store = {}

    async def dispatch(self, request: Request, call_next):
        # ignore docs and open root
        if request.url.path.startswith('/docs') or request.url.path.startswith('/openapi.json') or request.url.path == '/':
            return await call_next(request)
        client = request.client.host if request.client else 'unknown'
        now = time.time()
        window_start = now - self.window
        hits = self.store.get(client, [])
        # keep only recent hits
        hits = [t for t in hits if t > window_start]
        if len(hits) >= self.max_requests:
            return JSONResponse(status_code=429, content={
                'status': 'error',
                'error': {
                    'code': 'RATE_LIMIT_EXCEEDED',
                    'message': 'Too many requests'
                }
            })
        hits.append(now)
        self.store[client] = hits
        return await call_next(request)
