from app.utils import rate_limiter

def test_rate_limiter_allows_five_requests(client):
    for _ in range(5):
        response = client.get(f'/api/messages/message-12345')
    assert response.status_code == 200
    
def test_rate_limiter_blocks_after_max_requests(client):
    for _ in range(6):
        response = client.get(f'/api/messages/message-12345')
    data = response.json()
    assert response.status_code == 429
    assert data['status'] == 'error'
    assert data['error']['message'] == 'Demasiadas peticiones'