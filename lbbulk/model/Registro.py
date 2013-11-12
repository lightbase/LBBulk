from sqlalchemy import Table, Column, Integer, \
        String, join, ForeignKey
from sqlalchemy.orm import column_property
from lbbulk.model import Base, metadata

# define two Table objects
bulk_sources = Table('lb_bulk_sources', metadata,
            Column('id_source', Integer, primary_key=True),
            Column('nome_source', String),
        )

bulk_upload = Table('lb_bulk_upload', metadata,
            Column('id_reg', Integer, primary_key=True),
            Column('chave_externa', String),
            Column('id_source', Integer, ForeignKey('lb_bulk_sources.id_source'))
            )

# define a join between them.  This
# takes place across the bulk_sources.id_source and bulk_upload.id_source
# columns.
registro = join(bulk_sources, bulk_upload)

# map to it
class Registro(Base):
    __table__ = registro
    id_source = column_property(bulk_sources.c.id_source, bulk_upload.c.id_source)