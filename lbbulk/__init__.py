
from pyramid.config import Configurator
from lbbulk import config


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    configurator = Configurator(settings=settings)

    config.setup_config(settings)
    config.make_routes(configurator)
    configurator.scan()

    return configurator.make_wsgi_app()
