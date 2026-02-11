from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
SQL_ALCHEMY_DATABASE_URL=settings.database_url
engine=create_engine(SQL_ALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(bind=engine,autoflush=False)

def get_db():
    db=SessionLocal()
    try:
        yield db #here database is called 
    finally:
        db.close()    