from sqlalchemy import Table, Column, Integer, String
from pyramid_restler.model import SQLAlchemyORMContext
from lbbulk.model import Base, metadata, session


bulk_sources = Table('lb_bulk_sources', metadata,
                     Column('id_source', Integer, primary_key=True),
                     Column('nome_source', String, nullable=False)
                    )


# map to it
class BulkSources(Base):
    __table__ = bulk_sources

class BulkSourcesContextFactory(SQLAlchemyORMContext):
    entity = BulkSources

    def session_factory(self):
        return session