from sqlalchemy import Table, Column, Integer, String, ForeignKey
from requests import get
from pyramid_restler.model import SQLAlchemyORMContext
from lbbulk.model import Base, metadata, session
import json


bulk_upload = Table('lb_bulk_upload', metadata,
                    Column('id_reg', Integer, primary_key=True),
                    Column('external_key', String, nullable=False),
                    Column('id_source', Integer,
                           ForeignKey('lb_bulk_source.id_source'),
                           nullable=False),
                    extend_existing=True
                   )

# map to it
class BulkUpload(Base):
    __table__ = bulk_upload

    def verifica_registro(data):
        # q = session.query(BulkUpload).filter_by(id_source=1, external_key=data['json_reg']['id_reg'] )
        get('localhost/')
        registro_existe = q.first()
        if sim:
            registro_existe = True
        else:
            registro_existe = False
        return registro_existe


class BulkUploadContextFactory(SQLAlchemyORMContext):
    entity = BulkUpload

    def session_factory(self):
        return session

    def get_member_id_as_string(self, member):
        id = self.get_member_id(member)
        return json.dumps(id, cls=self.json_encoder)