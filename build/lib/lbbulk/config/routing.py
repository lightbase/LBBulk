from lbbulk.model.Registo import RegistroContextFactory

def make_routes(config):
    """
    Create routes
    """
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_restful_routes('registo', Registo.RegistroContextFactory)