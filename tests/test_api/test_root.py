from fastapi.testclient import TestClient
from solo_plai.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint returns the expected message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to Solo Plai API" in response.json()["message"]
