from app.service import process_message
from datetime import datetime
import pytest

def test_process_message_counts():
    payload = {
        'message_id': 'm1',
        'session_id': 's1',
        'content': 'Hola mundo',
        'timestamp': datetime.utcnow(),
        'sender': 'user'
    }
    out = process_message(payload)
    assert out['metadata']['word_count'] == 2
    assert out['metadata']['character_count'] == len('Hola mundo')

def test_process_message_inappropriate():
    payload = {
        'message_id': 'm2',
        'session_id': 's2',
        'content': 'esto contiene mala1 palabra',
        'timestamp': datetime.utcnow(),
        'sender': 'user'
    }
    with pytest.raises(Exception) as excinfo:
        process_message(payload)
    assert 'INAPPROPRIATE_CONTENT' in str(excinfo.value)
