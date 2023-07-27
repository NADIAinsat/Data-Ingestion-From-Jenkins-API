# This class will connect to the database and store the job and build info
import pyodbc as odbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = 'PC-NADIA\MSSQLSERVER19'

DATABASE_NAME = 'mydb'

connection_string = f"""
        DRIVER={DRIVER_NAME};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        Trusted_Connection=yes;
"""

connection = odbc.connect(connection_string)
cursor = connection.cursor()
# Create the database engine
engine = create_engine('mssql+pyodbc://', creator=lambda: connection)
# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()
print(connection)
