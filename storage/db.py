import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

file_config = pathlib.Path(__file__).parent.joinpath('config.ini')  # config-file path
SQLALCHEMY_DATABASE = 'SQLITE'  # set the database


def get_db_credentials(db_header: str = 'POSTGRES', file_config: str = None):
    config = configparser.ConfigParser()
    r = config.read(file_config)
    if db_header == 'POSTGRES':
        username = config.get('POSTGRES', 'USER')
        password = config.get('POSTGRES', 'PASSWORD')
        database_name = config.get('POSTGRES', 'DB_NAME')
        domain = config.get('POSTGRES', 'DOMAIN')
        port = config.get('POSTGRES', 'PORT')
        url = f'postgresql://{username}:{password}@{domain}:{port}/{database_name}'
        return url
    elif db_header == 'SQLITE':
        file_name = config.get('SQLITE', 'FILE_NAME')
        file_path = config.get('SQLITE', 'PATH')
        url = f'sqlite:///{file_path}{file_name}'
        return url


# connect to DB SQLite
DATABASE_URL = get_db_credentials(SQLALCHEMY_DATABASE, file_config)


# print(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=False)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = DBSession()
