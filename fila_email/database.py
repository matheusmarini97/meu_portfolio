from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import connection_string

engine = create_engine(connection_string(), echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()