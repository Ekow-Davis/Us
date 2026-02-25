from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # set False later for production, True for development
    pool_pre_ping=True,
    pool_recycle=300,  # recycle connections after 5 minutes
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
