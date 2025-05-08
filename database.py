from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import config
from models import BaseDB

engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

BaseDB.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()