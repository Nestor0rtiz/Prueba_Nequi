from sqlalchemy.orm import Session
from . import models
import datetime

def create_message(db: Session, msg_data: dict):
    m = models.Message(
        message_id = msg_data['message_id'],
        session_id = msg_data['session_id'],
        content = msg_data['content'],
        timestamp = msg_data['timestamp'],
        sender = msg_data['sender'],
        word_count = msg_data['metadata']['word_count'],
        character_count = msg_data['metadata']['character_count'],
        processed_at = msg_data['metadata']['processed_at']
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

def get_messages(db: Session, session_id: str, limit: int = 50, offset: int = 0, sender: str | None = None, search: str | None = None):
    q = db.query(models.Message).filter(models.Message.session_id == session_id)
    if sender:
        q = q.filter(models.Message.sender == sender)
    if search:
        q = q.filter(models.Message.content.ilike(f"%{search}%"))
    q = q.order_by(models.Message.timestamp).offset(offset).limit(limit)
    return q.all()
