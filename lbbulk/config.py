# -*- coding: utf-8 -*-
def setup_config(settings):

    global EXTRACT_DIR
    global JSON_FILENAME
    global LIGHTBASE_URL
    global HOST_DB
    global DATABASE_DB
    global USER_DB
    global PASSWORD_DB

    EXTRACT_DIR = settings['extract_dir']
    JSON_FILENAME = settings['json_filename']
    LIGHTBASE_URL = settings['lightbase_url']
    HOST_DB = settings['host']
    DATABASE_DB = settings['database']
    USER_DB = settings['user']
    PASSWORD_DB = settings['password']

def make_routes(cfg):

    from lbbulk.view import zip_upload

    cfg.add_route('zip_upload', 'zip_upload', request_method='POST')
    cfg.add_view(view=zip_upload, route_name='zip_upload')
