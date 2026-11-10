from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DATABASEURL = os.getenv("DATABASE_URL")
if not DATABASEURL:
    raise ValueError("DATABASE_URL missing. Create .env using .env.example")
engine = create_engine(DATABASEURL)
sessionlocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
base = declarative_base()
