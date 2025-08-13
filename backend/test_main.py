import sys
import os
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_topic():
    """
    Test case for creating a new topic.
    """
    response = client.post(
        "/topics/",
        json={
            "name": "Test Topic",
            "keywords": ["test", "fastapi"],
            "related_items": ["pytest"],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Topic"
    assert data["keywords"] == ["test", "fastapi"]
    assert "id" in data

def test_list_topics_empty():
    """
    Test case for listing topics when none exist.
    """
    response = client.get("/topics/")
    assert response.status_code == 200
    assert response.json() == []

def test_list_topics_with_data():
    """
    Test case for listing all topics.
    """
    client.post("/topics/",json={"name": "Topic 1", "keywords": [], "related_items": []})
    client.post("/topics/",json={"name": "Topic 2", "keywords": [], "related_items": []})

    response = client.get("/topics/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_get_topic():
    """
    Test case for getting a single topic by its ID.
    """
    create_response = client.post("/topics/", json={"name": "Another Topic", "keywords": [], "related_items": []})
    topic_id = create_response.json()["id"]

    response = client.get(f"/topics/{topic_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Another Topic"
    assert data["id"] == topic_id

def test_get_non_existent_topic():
    """
    Test case for getting a topic that does not exist.
    """
    response = client.get("/topics/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Topic not found"}

def test_update_topic():
    """
    Test case for updating an existing topic.
    """
    create_response = client.post("/topics/", json={"name": "Update Me", "keywords": ["original"], "related_items": []})
    topic_id = create_response.json()["id"]

    update_data = {
        "name": "Updated Name",
        "keywords": ["updated"],
        "related_items": ["new_item"],
    }
    response = client.put(f"/topics/{topic_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["keywords"] == ["updated"]
    assert data["id"] == topic_id

def test_delete_topic():
    """
    Test case for deleting a topic.
    """
    create_response = client.post("/topics/", json={"name": "Delete Me", "keywords": [], "related_items": []})
    topic_id = create_response.json()["id"]

    response = client.delete(f"/topics/{topic_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/topics/{topic_id}")
    assert get_response.status_code == 404

def test_delete_non_existent_topic():
    """
    Test case for deleting a topic that does not exist.
    """
    response = client.delete("/topics/9999")
    assert response.status_code == 404

def test_get_literature_placeholder():
    """
    Test the placeholder literature endpoint.
    """
    response = client.get("/literature/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2 # As per mock data

def test_get_ppt_history_placeholder():
    """
    Test the placeholder PPT history endpoint.
    """
    response = client.get("/ppt-history/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1 # As per mock data
