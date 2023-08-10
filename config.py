import configparser
import os

config = configparser.ConfigParser()
config['Jenkins'] = {'jenkins_url': os.environ.get('jenkins_url'),
                     'jenkins_username': os.environ.get('jenkins_username'),
                     'jenkins_password': os.environ.get('jenkins_password')}

config['Database'] = {'DRIVER_NAME': 'ODBC Driver 17 for SQL Server',
                      'SERVER_NAME': 'PC-NADIA\MSSQLSERVER19',
                      'DATABASE_NAME': 'mydb'}

jobs_names_list = []
