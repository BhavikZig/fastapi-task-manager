from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

engine = create_engine(settings.database_url)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()