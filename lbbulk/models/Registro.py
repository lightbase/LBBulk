from sqlalchemy import Table, Column, Integer, \
        String, MetaData, join, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property

metadata = MetaData()

# define two Table objects
bulk_sources = Table('lb_bulk_sources', metadata,
            Column('id_source', Integer, primary_key=True),
            Column('nome_source', String),
        )

bulk_upload = Table('lb_bulk_upload', metadata,
            Column('id_reg', Integer, primary_key=True),
            Column('chave_externa', String)
            Column('id_source', Integer, ForeignKey('lb_bulk_sources.id_source')),
            )

# define a join between them.  This
# takes place across the user.id and address.user_id
# columns.
user_address_join = join(user_table, address_table)

Base = declarative_base()

# map to it
class AddressUser(Base):
    __table__ = user_address_join

    id = column_property(user_table.c.id, address_table.c.user_id)
    address_id = address_table.c.id