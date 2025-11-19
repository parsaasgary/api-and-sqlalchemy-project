from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"massage" : "API works fine"}

def test_read_players():
    response = client.get("/v0/players/?skip=0&limit=10000")
    assert response.status_code == 200
    assert len(response.json()) == 1018

def test_read_players_with_name():
    response = client.get("/v0/players/?player_first_name=Bryce&player_last_name=Young")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get("player_id") == 2009

def test_read_player_with_id():
    response = client.get("/v0/player/1001")
    assert response.status_code == 200
    assert response.json().get("player_id") == 1001

def test_get_performances():
    response = client.get("/v0/performance/?skip=0&limit=20000")
    assert response.status_code == 200
    assert len(response.json()) == 17306

def test_get_performance_by_date():
    response = client.get("/v0/performance/?skip=0&limit=20000&min_last_date_changed=2024-04-01")
    assert response.status_code == 200
    assert len(response.json()) == 2711

def test_get_leagues():
    response = client.get("/v0/leagues/?skip=0&limit=500")
    assert response.status_code == 200
    assert len(response.json()) == 5

def test_get_league_by_id():
    response = client.get("/v0/league/5002")
    assert response.status_code == 200
    assert len(response.json()["teams"]) == 8


def test_read_teams():
    response = client.get("/v0/teams/?skip=0&limit=500")
    assert response.status_code == 200
    assert len(response.json()) == 20



def test_read_teams_for_one_league():
    response = client.get("/v0/teams/?skip=0&limit=500&league_id=5001")
    assert response.status_code == 200
    assert len(response.json()) == 12



def test_counts():
    response = client.get("/v0/counts/")
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["league_count"] == 5
    assert response_data["team_count"] == 20
    assert response_data["player_count"] == 1018