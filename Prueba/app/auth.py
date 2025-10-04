import os
from fastapi import Header, HTTPException, Depends
from starlette.status import HTTP_401_UNAUTHORIZED

API_KEY = os.getenv('API_KEY', 'changeme123')

async def api_key_dependency(x_api_key: str = Header(None)):
    if x_api_key is None or x_api_key != API_KEY:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail={
            'status': 'error',
            'error': {
                'code': 'UNAUTHORIZED',
                'message': 'API key missing or invalid'
            }
        })
    return True
