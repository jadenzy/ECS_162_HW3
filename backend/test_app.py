import pytest
from app import app as flask_app
from unittest.mock import patch, MagicMock
from bson import ObjectId
import json

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def mock_user_session(client, name='testuser'):
    with client.session_transaction() as sess:
        sess['user'] = {"name": name}

@patch("app.db")
def test_get_key(mock_db, client):
    response = client.get("/api/key")
    assert response.status_code == 200
    assert "apiKey" in response.json

@patch("app.db")
def test_get_articles(mock_db, client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "response": {
            "docs": [
                {"web_url": "http://example.com/1", "headline": {"main": "Test Article 1"}},
                {"web_url": "http://example.com/2", "headline": {"main": "Test Article 2"}}
            ]
        }
    }
    with patch("app.requests.get", return_value=mock_response):
        response = client.get("/api/articles")
        assert response.status_code == 200
        assert "articles" in response.json
        assert len(response.json["articles"]) == 2

@patch("app.db")
def test_post_comment(mock_db, client):
    mock_user_session(client, name="testuser")
    mock_insert = mock_db.comments.insert_one

    payload = {
        "article_id": "123456",
        "text": "This is a comment",
        "parent_id": None
    }

    response = client.post("/api/comments", json=payload)
    assert response.status_code == 201
    mock_insert.assert_called_once()

@patch("app.db")
def test_get_comments(mock_db, client):
    mock_db.comments.find.return_value = [
        {"_id": ObjectId("507f1f77bcf86cd799439011"), "article_id": "123", "text": "Hello"}
    ]
    response = client.get("/api/comments?article_id=123")
    assert response.status_code == 200
    assert isinstance(response.json, list)

@patch("app.db")
def test_delete_comment_author(mock_db, client):
    mock_user_session(client, name="author")
    mock_db.comments.find_one.return_value = {
        "_id": ObjectId("507f1f77bcf86cd799439011"), "user": "author"
    }
    response = client.delete("/api/comments?id=507f1f77bcf86cd799439011")
    assert response.status_code == 200
    mock_db.comments.delete_one.assert_called_once()

@patch("app.db")
def test_delete_comment_forbidden(mock_db, client):
    mock_user_session(client, name="user1")
    mock_db.comments.find_one.return_value = {
        "_id": ObjectId("507f1f77bcf86cd799439011"), "user": "other_user"
    }
    response = client.delete("/api/comments?id=507f1f77bcf86cd799439011")
    assert response.status_code == 403

@patch("app.db")
def test_redact_comment_by_moderator(mock_db, client):
    mock_user_session(client, name="moderator")
    comment_id = "507f1f77bcf86cd799439011"
    response = client.patch("/api/comments", json={"id": comment_id, "text": "sensitive content"})
    assert response.status_code == 200
    mock_db.comments.update_one.assert_called_once()

def test_user_not_logged_in(client):
    response = client.get("/api/user")
    assert response.status_code == 401

def test_user_logged_in(client):
    mock_user_session(client, name="testuser")
    response = client.get("/api/user")
    assert response.status_code == 200
    assert response.json["name"] == "testuser"

