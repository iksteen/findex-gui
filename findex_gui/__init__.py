from pyramid.config import Configurator
from pyramid_sqlalchemy import Session

from findex_gui.db.orm import initialize_pyramid_sqlalchemy


def db_file_count(request):
    return int(Session.execute("""
        SELECT reltuples::int FROM pg_class WHERE relname ='files'
    """).first()[0])


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_tm')
    initialize_pyramid_sqlalchemy(config)

    config.add_static_view(name='static', path='findex_gui:static')

    config.add_route('home', '/')
    config.add_route('search', '/search')
    config.add_route('terms', '/terms')

    config.add_route('robots', '/robots.txt')
    config.add_route('favicon', '/favicon.ico')

    config.scan('findex_gui.views')

    config.add_request_method(db_file_count, 'db_file_count', True, True)

    return config.make_wsgi_app()
