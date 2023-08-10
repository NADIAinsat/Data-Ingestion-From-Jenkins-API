# This class will connect to the database and store the job and build info
import pyodbc as odbc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config


DRIVER_NAME = config.config['Database']['DRIVER_NAME']
SERVER_NAME = config.config['Database']['SERVER_NAME']
DATABASE_NAME = config.config['Database']['DATABASE_NAME']

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
