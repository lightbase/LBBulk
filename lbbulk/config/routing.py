# import lbbulk.model
from lbbulk.model.Registro import RegistroContextFactory
from lbbulk.view.restfulview import RegCustomView

def make_routes(config):
    """
    Create routes
    """
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_restful_routes('registro', RegistroContextFactory, view=RegCustomView)