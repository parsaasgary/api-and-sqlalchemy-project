import sys
from pathlib import Path

# Add parent directory to Python path to allow importing Database module
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from fastapi import FastAPI , Depends , HTTPException , Query
from sqlalchemy.orm import Session
from datetime import date


from . import schemas
import Database.CRUD as crud
from Database.create_db_and_tabels import engine


api_description ="""
this api is created from the data of a fottbal fantasy league
this is more of a sqlalchemy and fast api mini project for me

it has 4 kind of api responses:
## Analytics
Get information about health of the API and counts of leagues, teams, and players.

## Player
You can get a list of an NFL players, or search for an individual player by player_id.

## Scoring
You can get a list of NFL player performances, including the fantasy points they scored using SWC league scoring.

## Membership
Get information about all the SWC fantasy football leagues and the teams in them.

"""

app = FastAPI(
    description= api_description,
    title= " fastapi mini project(footbal fantasy api)",
    version="0.1"
)

def db_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

@app.get("/",
         summary="checking the health of the api",
         description="""this is the root of the api for checking the health of the api and it's creation""",
         response_description="""it will return a simple json massage """,
         tags=["Analytics"],
         operation_id="v0_healthcheck",)

async def root():
    return {"massage" : "API works fine"}

@app.get("/v0/players/" , response_model=list[schemas.Player],
         summary="This api will return list of players",
         description="""base on the date or player first and last name will return a list of players
         the number of players in the list can be handeled by the skip and limit values""",
         tags= ["Player"],
         response_description="""the return values is a list of players in the footbal fantasy league""",
         operation_id = "v0_get_players",)
def read_players(
    skip : int = Query( 0 , description="from which point of the beggining it return the players"),
    limit : int = Query( 100 , description="how many players be included"),
    min_last_changed_date : date = Query( None , description="choose return the players from this date up to now") ,
    player_first_name : str = Query( None , description="the first name of players to return") ,
    player_last_name : str = Query( None , description="the last name of players to return") , 
    db : Session = Depends(db_session)
    ):
    players = crud.get_players(db , skip , limit , min_last_changed_date
                               ,player_first_name,player_last_name)
    return players

@app.get("/v0/player/{player_id}" , response_model=schemas.Player,
         summary="get a player by it id",
         description="""this api will return ONLY a player and his information by having it's player id""",
         operation_id="v0_get_player_by_id",
         tags=["PLayer"],
         response_description="""a single player and all it information(league , first name , last name etc)""",
         )
def read_player(player_id : int , db : Session = Depends(db_session) ):
    player = crud.get_player(db , player_id)
    if player is None:
        raise HTTPException(status_code=404 , detail="player not found")
    return player

@app.get("/v0/performance/" , response_model=list[schemas.Performance],
     summary="Get all the weekly performances that meet all the parameters you sent ",
    description="""Use this api to get lists of weekly performances by players in the . You us the skip and limit to perform pagination of the API. Don't use the Performance ID for counting or logic, because that is an internal ID and is not guaranteed to be sequential""",
    response_description="A list of weekly scoring performances. It may be by multiple players.",
    operation_id="v0_get_performances",
    tags=["scoring"],)
def read_performances(min_last_date_changed : date = Query(0 , description="decide you want the result from which date"),
                      skip : int = Query( 0 , description="from which point of the beggining it return the performances") ,
                      limit : int = Query( 100 , description="how many of the performances you request"),
                      db : Session = Depends(db_session)):
    performances = crud.get_performances(db , min_last_date_changed,
                                         skip , limit
                                         )
    return performances
@app.get("/v0/leagues/", response_model=list[schemas.League],
    summary="Get all the SWC fantasy football leagues that match the parameters you send",
    description="""Use this endpoint to get lists of SWC fantasy football leagues. You us the skip and limit to perform pagination of the API. League name is not guaranteed to be unique. Don't use the League ID for counting or logic, because that is an internal ID and is not guaranteed to be sequential""",
    response_description="A list of leagues on the SWC fantasy football website.",
    operation_id="v0_get_leagues",
    tags=["membership"],)
def read_leagues(min_last_date_changed : date = Query(None,description="The minimum data of change that you want to return records. Exclude any records changed before this.",),
                 skip : int =Query(0, description="The number of items to skip at the beginning of API call."), 
                 limit : int = Query(100, description="The number of records to return after the skipped records.") ,
                 league_name : str = Query(None, description="Name of the leagues to return. Not unique in the SWC.") ,
                 db : Session = Depends(db_session)):
    leagues = crud.get_leagues(db , min_last_date_changed , skip , limit , league_name)
    return leagues

@app.get("/v0/league/{league_id}" , response_model= schemas.League,
    summary="Get one league by league id",
    description="""Use this endpoint to get a single league that matches the league ID provided by the user.""",
    response_description="An SWC league",
    operation_id="v0_get_league_by_league_id",
    tags=["membership"],)
def read_league(league_id : int = 0 , db: Session = Depends(db_session)):
    league = crud.get_league(db , league_id)
    if league is None:
        raise HTTPException(status_code="404" , detail="league didn't found")
    return league

@app.get("/v0/teams/", response_model=list[schemas.Team],
    summary="Get all the SWC fantasy football teams that match the parameters you send",
    description="""Use this endpoint to get lists of SWC fantasy football teams. You us the skip and limit to perform pagination of the API. Team name is not guaranteed to be unique. If you get the Team ID from another query such as v0_get_players, you can match it with the Team ID from this query.  Don't use the Team ID for counting or logic, because that is an internal ID and is not guaranteed to be sequential""",
    response_description="A list of teams on the SWC fantasy football website.",
    operation_id="v0_get_teams",
    tags=["membership"],)
def read_teams(skip: int = Query(0, description="The number of items to skip at the beginning of API call."), 
               limit: int = Query(100, description="The number of records to return after the skipped records."), 
               minimum_last_changed_date: date = Query(None,description="The minimum data of change that you want to return records. Exclude any records changed before this."), 
               team_name: str = Query(None,description="Name of the teams to return. Not unique across SWC, but is unique inside a league.",), 
               league_id: int = Query(None, description="League ID of the teams to return. Unique in SWC."), 
               db: Session = Depends(db_session)):
    teams = crud.get_teams(db, 
                offset=skip, 
                limit=limit, 
                min_last_date_change=minimum_last_changed_date, 
                team_names=team_name,
                league_id=league_id)
    return teams


@app.get("/v0/counts/", response_model=schemas.Count,

    summary="Get counts of the number of leagues, teams, and players in the SWC fantasy football",
    description="""Use this endpoint to count the number of leagues, teams, and players in the SWC fantasy football. Use in combination with skip and limit in v0_get leagues, v0_get_teams, or v0_get_players. Use this endpoint to get counts instead of making calls to the other APIs.""",
    response_description="A list of teams on the SWC fantasy football website.",
    operation_id="v0_get_counts",
    tags=["analytics"],)
def get_count(db: Session = Depends(db_session)):
    counts = schemas.Count(
        league_count = crud.get_leagues_count(db),
        team_count = crud.get_teams_count(db),
        player_count = crud.get_players_count(db))
    return counts