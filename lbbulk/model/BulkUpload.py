from sqlalchemy import Table, Column, Integer, String, ForeignKey
from pyramid_restler.model import SQLAlchemyORMContext
from lbbulk.model import Base, metadata, session
import json


bulk_upload = Table('lb_bulk_upload', metadata,
                    Column('id_reg', Integer, primary_key=True),
                    Column('chave_externa', String, nullable=False),
                    Column('id_source', Integer,
                           ForeignKey('lb_bulk_sources.id_source'),
                           nullable=False),
                    extend_existing=True
                   )

# map to it
class BulkUpload(Base):
    __table__ = bulk_upload

    def verifica_registro(data):
#        q = session.query(BulkUpload).filter_by(id_source=data['id_source'], chave_externa=data['json_reg']['id_reg'] )
        q = session.query(BulkUpload).filter_by(id_source=1, chave_externa=data['json_reg']['id_reg'] )
        registro_existe = q.first()
        return registro_existe


class BulkUploadContextFactory(SQLAlchemyORMContext):
    entity = BulkUpload

    def session_factory(self):
        return session

    def get_member_id_as_string(self, member):
        id = self.get_member_id(member)
        return json.dumps(id, cls=self.json_encoder)
