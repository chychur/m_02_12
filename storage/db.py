import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#postgresql://username:password@host:port/database_name
file_config = pathlib.Path(__file__).parent.joinpath('config.ini')

config = configparser.ConfigParser()
r = config.read(file_config)

username = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
database_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')
port = config.get('DB', 'PORT')
url = f'postgresql://{username}:{password}@{domain}:{port}/{database_name}'

engine = create_engine(url, echo=False)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = DBSession()
