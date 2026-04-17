from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

connection_string = (
    "Driver=ODBC Driver 17 for SQL Server;"
    "Server=(localdb)\\MSSQLLocalDB;"
    "Database=todosapp;"
    "Trusted_Connection=yes;"
)

SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={connection_string}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
