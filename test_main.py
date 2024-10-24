from fastapi.testclient import TestClient
from main import app

# Create TestClient instance
client = TestClient(app=app)


# Test function to get all blogs (http://127.0.0.1:8000/blog/all)
def test_get_all_blogs():
    response = client.get('/blog/all')
    assert response.status_code == 200