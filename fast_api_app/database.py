from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config
import databases

DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

database = databases.Database(DATABASE_URL)
Base: DeclarativeMeta = declarative_base()
engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
