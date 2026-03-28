from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="admin"
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS fastapi_task5")
conn.select_db("fastapi_task5")

# Load environment variables
load_dotenv()

# Get DB URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine (MySQL connection)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # helps avoid connection errors
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()