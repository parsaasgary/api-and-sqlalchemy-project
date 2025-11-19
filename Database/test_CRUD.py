import pytest
from .create_db_and_tabels import engine
from sqlalchemy.orm import Session
from datetime import date

import CRUD

test_date = date(2024 , 4, 1)

@pytest.fixture(scope="function")
def db_session():
    session = Session(engine)
    try:
        yield session
        session.rollback()  # Rollback any changes made during the test
    finally:
        session.close()

def test_get_player(db_session):
    player = CRUD.get_player(db_session, player_id=1001)
    assert player.player_id == 1001

def test_get_players(db_session):
    players = CRUD.get_players(db_session, skip=0, limit=10000,
                                min_last_changed_date=test_date)
    assert len(players) == 1018

def test_get_players_by_name(db_session):
    players = CRUD.get_players(db_session, player_first_name="Bryce", player_last_name="Young")
    assert len(players) == 1
    assert players[0].player_id == 2009


def test_get_all_performances(db_session):
    performances = CRUD.get_performances(db_session, offset=0, limit=18000)
    assert len(performances) == 17306

def test_get_new_performances(db_session):
    performances = CRUD.get_performances(db_session, offset=0, limit=10000, 
                                         min_last_date_changed=test_date)
    assert len(performances) == 2711

def test_get_league(db_session):
    league = CRUD.get_league(db_session, league_id = 5002)
    assert league.league_id == 5002
    assert len(league.teams) == 8



def test_get_leagues(db_session):
    leagues = CRUD.get_leagues(db_session, offset=0, limit=10000, min_last_date_change=test_date)
    assert len(leagues) == 5


def test_get_teams(db_session):
    teams = CRUD.get_teams(db_session, offset=0, limit=10000, min_last_date_change=test_date)
    assert len(teams) == 20

def test_get_teams_for_one_league(db_session):
    teams = CRUD.get_teams(db_session, league_id=5001)
    assert len(teams) == 12
    assert teams[0].league_id == 5001

def test_get_team_players(db_session):
    first_team = CRUD.get_teams(db_session, offset=0, limit=1000, min_last_date_change=test_date)[0]
    assert len(first_team.Team_Players) == 7

#test the count functions
def test_get_player_count(db_session):
    player_count = CRUD.get_players_count(db_session)
    assert player_count == 1018

def test_get_team_count(db_session):
    team_count = CRUD.get_teams_count(db_session)
    assert team_count == 20

def test_get_league_count(db_session):
    league_count = CRUD.get_leagues_count(db_session)
    assert league_count == 5