import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# This test will only pass on the first run, later the shortcode will already exist and the test fails
def test_create_short_url():
  response = client.post("/shorten", json={"url": "https://www.w3schools.com/python/python_tuples.asp", "shortcode": "QWESA21_"})
  assert response.status_code == 201
  assert "shortcode" in response.json()
  
def test_create_short_url_without_url():
  response = client.post("/shorten", json={"url": "", "shortcode": "QWESA21_"})
  assert response.status_code == 400
  
def test_create_existing_short_url():
  response = client.post("/shorten", json={"url": "https://www.w3schools.com/python/python_lists.asp", "shortcode": "QWESA21_"})
  assert response.status_code == 409
  # assert response.details == "Shortcode already in use"
  
def test_create_invalid_short_url():
  response = client.post("/shorten", json={"url": "https://www.w3schools.com/python/python_lists.asp", "shortcode": "QWE"})
  assert response.status_code == 412
  # assert response.details == "The provided shortcode is invalid"
  
def test_redirect_to_original_url():
  response = client.get("/QWESA21_")
  assert response.status_code == 302
  assert response.headers["location"] == "https://www.w3schools.com/python/python_tuples.asp"

def test_redirect_to_origial_bad_url():
  response = client.get("/QWESA22321_")
  assert response.status_code == 404

# need to replace '{shortcode}' with an actual code from db
def test_get_stats():
  response = client.get("/QWESA21_/stats")
  assert response.status_code == 200