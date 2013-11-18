from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from lbbulk.config.routing import make_routes
from pyramid_restler import includeme

from lbbulk.model import Base, metadata, DBSession


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.scan('lbbulk')
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    includeme(config)
    config.include('pyramid_chameleon')
    make_routes(config)
    config.enable_POST_tunneling()
    return config.make_wsgi_app()