from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

metadata = MetaData()
Base = declarative_base()
DBSession = scoped_session(sessionmaker())