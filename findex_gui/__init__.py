from pyramid.config import Configurator
from pyramid_sqlalchemy import Session

from findex_gui.controllers.findex import themes
from findex_gui.db.orm import initialize_pyramid_sqlalchemy


def db_file_count(request):
    return int(Session.execute("""
        SELECT reltuples::int FROM pg_class WHERE relname ='files'
    """).first()[0])


def theme_name(request):
    return themes.DATA.get_theme()


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_tm')
    initialize_pyramid_sqlalchemy(config)
    config.include('pyramid_jinja2')

    themes.DATA = themes.Themes()

    config.add_jinja2_search_path('findex_gui:static/themes/findex_official/templates')

    config.add_static_view(name='static', path='findex_gui:static')

    config.add_route('home', '/')
    config.add_route('terms', '/terms')
    config.add_route('api', '/api')
    config.add_route('research', '/research')
    config.add_route('research-mass-ftp-crawling', '/research/mass-ftp-crawling')
    config.add_route('documentation', '/documentation')

    config.add_route('robots', '/robots.txt')
    config.add_route('favicon', '/favicon.ico')

    config.scan('findex_gui.views')
    config.scan('findex_gui.controllers.views')

    config.add_request_method(db_file_count, 'db_file_count', True, True)
    config.add_request_method(theme_name, 'theme_name', True, True)

    return config.make_wsgi_app()
