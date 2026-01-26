from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from app.core.config import settings
password = quote_plus(settings.database_password)
SQL_ALCHEMY_DATABASE_URL=f'postgresql+psycopg://{settings.database_username}:{password}@{settings.database_hostname}/{settings.database_name}'
engine=create_engine(SQL_ALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(bind=engine,autoflush=False)

def get_db():
    db=SessionLocal()
    try:
        yield db #here database is called 
    finally:
        db.close()    