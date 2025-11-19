from create_db_and_tabels import engine, Base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from pathlib import Path

# Force table creation first (only creates if not exist)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Read CSVs
league_data_Df = pd.read_csv(DATA_DIR / "league_data.csv")
performance_data_Df = pd.read_csv(DATA_DIR / "performance_data.csv")
player_data_Df = pd.read_csv(DATA_DIR / "player_data.csv")
team_data_Df = pd.read_csv(DATA_DIR / "team_data.csv")
team_player_data_Df = pd.read_csv(DATA_DIR / "team_player_data.csv")

# CRITICAL: Force correct dtypes before inserting
performance_data_Df["week_number"] = performance_data_Df["week_number"].astype(str)  # ← Force string
performance_data_Df["last_changed_date"] = pd.to_datetime(performance_data_Df["last_changed_date"])

player_data_Df["last_changed_date"] = pd.to_datetime(player_data_Df["last_changed_date"])
team_data_Df["last_changed_date"] = pd.to_datetime(team_data_Df["last_changed_date"])
league_data_Df["last_changed_date"] = pd.to_datetime(league_data_Df["last_changed_date"])
team_player_data_Df["last_changed_date"] = pd.to_datetime(team_player_data_Df["last_changed_date"])

# Now load with correct types and preserve SQLAlchemy schema
print("Loading data...")
league_data_Df.to_sql("league", con=engine, if_exists="append", index=False)
performance_data_Df.to_sql("performance", con=engine, if_exists="append", index=False)
player_data_Df.to_sql("player", con=engine, if_exists="append", index=False)
team_data_Df.to_sql("team", con=engine, if_exists="append", index=False)
team_player_data_Df.to_sql("team_player", con=engine, if_exists="append", index=False)

print("All data loaded successfully!")
session.close()