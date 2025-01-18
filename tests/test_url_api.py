import pytest
from fastapi.testclient import TestClient

def test_create_short_url(client: TestClient):
    response = client.post(
        "/shorten/",
        json={"original_url": "https://www.example.com/"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["original_url"].rstrip('/') == "https://www.example.com"
    assert "short_url" in data
    assert "full_url" in data
    assert data["clicks"] == 0

def test_redirect_to_url(client: TestClient):
    # Create a URL
    create_response = client.post(
        "/shorten/",
        json={"original_url": "https://www.example.com/"}
    )
    short_url = create_response.json()["short_url"]
    
    # Test redirect
    response = client.get(f"/{short_url}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"].rstrip('/') == "https://www.example.com"

def test_get_url_stats(client: TestClient):
    # Create a URL
    create_response = client.post(
        "/shorten/",
        json={"original_url": "https://www.example.com/"}
    )
    short_url = create_response.json()["short_url"]
    
    # Check stats
    response = client.get(f"/stats/{short_url}")
    assert response.status_code == 200
    data = response.json()
    assert data["original_url"].rstrip('/') == "https://www.example.com"
    assert data["short_url"] == short_url
    assert "clicks" in data

def test_get_nonexistent_url_stats(client: TestClient):
    response = client.get("/stats/nonexistent")
    assert response.status_code == 404 