from .create_db_and_tabels import engine , Player , Performance ,TeamPlayer ,Team , League
from sqlalchemy.orm import Session , joinedload 
from datetime import date


def get_player (db:Session , player_id : int):
    return db.query(Player).filter(Player.player_id == player_id).first()


def get_players (db:Session , skip: int = 0  , limit: int = 100  ,
                 min_last_changed_date : date = None ,
                 player_first_name : str = None,
                 player_last_name : str = None  ):
    
    query = db.query(Player)

    if min_last_changed_date:
        query = query.filter(Player.last_changed_date >= min_last_changed_date)
    if player_first_name:
        query = query.filter(Player.first_name == player_first_name)
    if player_last_name:
        query =  query.filter(Player.last_name == player_last_name)
    return query.offset(skip).limit(limit).all()

def get_performances (db:Session , min_last_date_changed : date = None,
                      offset : int = 0 , limit : int = 100 ):
    
    query = db.query(Performance)

    if min_last_date_changed:
        query = query.filter(Performance.last_changed_date >= min_last_date_changed)
    return query.offset(offset).limit(limit).all()

def get_league (db:Session , league_id : int = 0):
    return db.query(League).filter(League.league_id == league_id).first()

def get_leagues (db:Session , min_last_date_change : date = None,
                 offset : int = 0 , limit : int = 100 ,
                 league_name : str = None):
    
    query = db.query(League).options(joinedload(League.teams))

    if min_last_date_change:
        query = query.filter(League.last_changed_date >= min_last_date_change)
    if league_name:
        query = query.filter(League.league_name == league_name)
    return query.offset(offset).limit(limit).all()    

def get_teams (db:Session , min_last_date_change : date = None,
                 offset : int = 0 , limit : int = 100 ,
                 team_names : str = None , league_id: int = None):
    
    query = db.query(Team)

    if min_last_date_change:
        query = query.filter(Team.last_changed_date >= min_last_date_change)
    if team_names:
        query = query.filter(Team.team_name == team_names)
    if league_id:
        query = query.filter(Team.league_id == league_id)
    return query.offset(offset).limit(limit).all()

def get_players_count(db:Session):
    query = db.query(Player)
    return query.count()

def get_teams_count(db:Session):
    query = db.query(Team)
    return query.count()

def get_leagues_count(db:Session):
    query = db.query(League)
    return query.count()