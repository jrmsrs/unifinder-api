from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import Session
from app.infra.config import Settings

load_dotenv()
# DATABASE_URL = "sqlite:///./database.db"
DATABASE_URL = Settings.database_url

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(bind=engine, autoflush=False)
# Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session