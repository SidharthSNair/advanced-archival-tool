from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# For SQLite, need check_same_thread=False when accessed from multiple threads (dev)
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,            # set True if you want SQL in logs during debugging
    pool_pre_ping=True,    # validates connections before using them
    connect_args=connect_args,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
