from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    url='sqlite:///test.db',
    connect_args={'check_same_thread':False}
)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()