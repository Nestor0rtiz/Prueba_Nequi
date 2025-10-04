from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db, Base, engine
from .. import service, repository, schemas
from ..ws import broadcast_new_message
import datetime

router = APIRouter(prefix='/api/messages', tags=['messages'])

# Crear tablas si no existen (carga inicial)
Base.metadata.create_all(bind=engine)

@router.post('', response_model=schemas.MessageOut)
def post_message(msg: schemas.MessageIn, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        processed = service.process_message(msg.dict())
    except HTTPException as e:
        # Levantamos error con formato uniforme
        raise HTTPException(status_code=e.status_code, detail={
            'status': 'error',
            'error': e.detail
        })
    # Guardar en BD
    created = repository.create_message(db, processed)
    payload_out = {
        'status': 'success',
        'data': {
            'message_id': created.message_id,
            'session_id': created.session_id,
            'content': created.content,
            'timestamp': created.timestamp.isoformat(),
            'sender': created.sender,
            'metadata': {
                'word_count': created.word_count,
                'character_count': created.character_count,
                'processed_at': created.processed_at.isoformat()
            }
        }
    }
    # Notify websocket clients in background (if any)
    background_tasks.add_task(broadcast_new_message, created.session_id, {
        'message_id': created.message_id,
        'content': created.content,
        'timestamp': created.timestamp.isoformat(),
        'sender': created.sender
    })
    return payload_out

@router.get('/{session_id}', response_model=schemas.MessagesListOut)
def get_messages(session_id: str,
                 limit: int = Query(50, ge=1, le=200),
                 offset: int = Query(0, ge=0),
                 sender: str | None = Query(None),
                 search: str | None = Query(None),
                 db: Session = Depends(get_db)):
    results = repository.get_messages(db, session_id, limit, offset, sender, search)
    data = []
    for m in results:
        data.append({
            'message_id': m.message_id,
            'session_id': m.session_id,
            'content': m.content,
            'timestamp': m.timestamp.isoformat(),
            'sender': m.sender,
            'metadata': {
                'word_count': m.word_count,
                'character_count': m.character_count,
                'processed_at': m.processed_at.isoformat()
            }
        })
    return {'status': 'success', 'data': data, 'pagination': {'limit': limit, 'offset': offset}}
