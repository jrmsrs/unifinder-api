from sqlalchemy import create_engine
from sqlmodel import Session
from app.infra.config import Settings

DATABASE_URL = Settings.database_url


engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True
)

def get_session():
    with Session(engine) as session:
        yield session