from app import app

def test_movies():
    client = app.test_client()
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
