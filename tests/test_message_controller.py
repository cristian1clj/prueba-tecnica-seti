from app.schemas.message_schemas import MessageCreate
from datetime import datetime, timezone
import pytest

MESSAGE_BODY = {
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hola, ¿cómo puedo ayudarte hoy?",
    "timestamp": "2023-06-15T14:30:00Z",
    "sender": "system"
}

def test_create_message_success(client):
    response = client.post('/api/messages', json=MESSAGE_BODY)
    data = response.json()
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert data['data']['message_id'] == MESSAGE_BODY['message_id']

def test_create_message_duplicate_message_id_returns_error(client):
    client.post('/api/messages', json=MESSAGE_BODY)
    response = client.post('/api/messages', json=MESSAGE_BODY)
    data = response.json()
    assert response.status_code == 409
    assert data['status'] == 'error'
    assert MESSAGE_BODY['message_id'] in data['error']['details']

def test_create_message_incomplete_fields_returns_error(client):
    incomplete_message_body = {i: j for i, j in MESSAGE_BODY.items() if i != "timestamp"}
    response = client.post('/api/messages', json=incomplete_message_body)
    data = response.json()
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert data['error']['message'] == 'Formato de mensaje inválido'
    assert data['error']['details'] == 'El campo timestamp es obligatorio'

def test_get_messages_return_success(client):
    client.post('/api/messages', json=MESSAGE_BODY)
    response = client.get(f'/api/messages/{MESSAGE_BODY["session_id"]}')
    data = response.json()
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['total'] == len(data['data'])

def test_get_messages_filtered_by_incorrect_sender_returns_error(client):
    response = client.get(f'/api/messages/{MESSAGE_BODY["session_id"]}?sender=asdasd')
    data = response.json()
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert data['error']['details'] == "El parametro 'sender' debe ser 'user' o 'system'"