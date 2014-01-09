from sqlalchemy import Table, Column, Integer, String
from pyramid_restler.model import SQLAlchemyORMContext
from lbbulk.model import Base, metadata, session


bulk_source = Table('lb_bulk_source', metadata,
                     Column('id_source', Integer, primary_key=True),
                     Column('nome_source', String, nullable=False)
                    )


# map to it
class BulkSource(Base):
    __table__ = bulk_source

class BulkSourceContextFactory(SQLAlchemyORMContext):
    entity = BulkSource

    def session_factory(self):
        return session
