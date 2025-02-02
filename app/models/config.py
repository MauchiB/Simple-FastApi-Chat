from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB = os.getenv('POSTGRES_DB')
USER = os.getenv('POSTGRES_USER')
HOST = os.getenv('POSTGRES_HOST')
PORT = os.getenv('POSTGRES_PORT', '5432')

engine = create_engine(
    url=f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()