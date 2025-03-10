from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:212202@localhost:5432/cinematch")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
