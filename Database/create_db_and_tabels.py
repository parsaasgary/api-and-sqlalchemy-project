from sqlalchemy import Column ,Float, Integer , String , ForeignKey , create_engine , DateTime , func
from sqlalchemy.orm import declarative_base , relationship
import os

Base = declarative_base()

class Player (Base):
    __tablename__ = "player"

    player_id = Column(Integer , nullable=False , primary_key=True)
    gsis_id   =  Column(String)
    first_name = Column(String(50) , nullable = False)
    last_name = Column(String(100) , nullable=False)
    position = Column(String(3), nullable=False )
    last_changed_date = Column(DateTime(timezone = True) , server_default=func.now() , nullable=False)

    performance = relationship("Performance" , back_populates="player")
    Team_Players = relationship("TeamPlayer" , back_populates="player")

class Performance (Base):
    __tablename__ = "performance"

    performance_id = Column(Integer , nullable=False , primary_key=True)
    week_number = Column(String ,  nullable=False)
    fantasy_points = Column(Float , nullable=False)
    player_id = Column(Integer ,  ForeignKey("player.player_id") , nullable=False )
    last_changed_date = Column(DateTime(timezone = True) , server_default=func.now() , nullable=False)

    player = relationship("Player" , back_populates="performance")

class League (Base):
    __tablename__ = "league"

    league_id = Column(Integer , nullable=False , primary_key=True)
    league_name = Column(String(50) , nullable=False)
    scoring_type = Column(String(50) , nullable=False)
    last_changed_date = Column(DateTime(timezone = True) , server_default=func.now() , nullable=False)

    teams = relationship("Team" , back_populates="league")

class Team (Base):
    __tablename__ = "team"

    team_id = Column(Integer , nullable=False , primary_key=True)
    team_name = Column(String , nullable=False )
    league_id = Column(Integer ,   ForeignKey("league.league_id") , nullable=False)
    last_changed_date = Column(DateTime(timezone = True) , server_default=func.now() , nullable=False)

    league = relationship("League" , back_populates="teams")
    Team_Players = relationship("TeamPlayer" , back_populates="team")

class TeamPlayer(Base):
    __tablename__ = "team_player"

    team_id = Column(Integer ,  ForeignKey("team.team_id") , nullable=False , primary_key=True)
    player_id = Column(Integer ,  ForeignKey("player.player_id") ,nullable=False,  primary_key=True)
    last_changed_date = Column(DateTime(timezone = True) , server_default=func.now() , nullable=False)

    team = relationship("Team" , back_populates="Team_Players")
    player = relationship("Player" , back_populates="Team_Players")


# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "fantasy_data.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL , echo=True , future=True , connect_args={"check_same_thread" : False})
Base.metadata.create_all(engine)
# print("Tables created successfully!")


