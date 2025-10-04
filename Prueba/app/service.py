from datetime import datetime
from fastapi import HTTPException
import re

# Lista simple de palabras prohibidas (personaliza según necesidad)
FORBIDDEN_WORDS = {"mala1", "mala2"}

def normalize_word(w: str) -> str:
    return re.sub(r"[^\w]", '', w).lower()

def process_message(payload: dict):
    content = payload.get('content', '')
    # split basic: separar por espacios
    words = [w for w in content.split() if w.strip()]
    normalized = [normalize_word(w) for w in words]
    found = [w for w in normalized if w in FORBIDDEN_WORDS]
    if found:
        # estructura de error para que coincida con el enunciado
        raise HTTPException(status_code=400, detail={
            'code': 'INAPPROPRIATE_CONTENT',
            'message': 'Contenido inapropiado detectado',
            'details': f'Palabras: {found}'
        })
    metadata = {
        'word_count': len(words),
        'character_count': len(content),
        'processed_at': datetime.utcnow()
    }
    result = dict(payload)
    result['metadata'] = metadata
    return result
