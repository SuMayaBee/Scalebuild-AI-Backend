import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Configure engine with connection pooling and SSL settings for Neon
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # This helps detect stale connections
    pool_recycle=300,    # Recycle connections every 5 minutes
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10,
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
