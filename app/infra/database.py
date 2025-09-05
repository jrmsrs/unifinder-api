import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import Session

load_dotenv()
# DATABASE_URL = "sqlite:///./database.db"
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./database.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(bind=engine, autoflush=False)
# Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session