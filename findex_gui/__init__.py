from pyramid.config import Configurator
from pyramid_sqlalchemy import Session

from findex_gui.db.orm import initialize_pyramid_sqlalchemy


THEMES = set()


def add_theme(config, theme):
    global THEMES
    THEMES.add(theme)


class ThemePredicate(object):
    def __init__(self, val, config):
        global THEMES
        if not val in THEMES:
            raise RuntimeError('No theme with that name exists.')

        self.val = val

    def text(self):
        return 'theme = %s' % (self.val,)

    phash = text

    def __call__(self, context, request):
        return request.theme == self.val


def current_theme(request):
    return 'findex_official'


def db_file_count(request):
    return int(Session.execute("""
        SELECT reltuples::int FROM pg_class WHERE relname ='files'
    """).first()[0])


def main(global_config, **settings):
    config = Configurator(settings=settings)

    config.add_directive('add_theme', add_theme)
    config.add_route_predicate('theme', ThemePredicate)

    config.add_request_method(db_file_count, 'db_file_count', True, True)
    config.add_request_method(current_theme, 'theme', True, True)

    config.include('pyramid_tm')
    initialize_pyramid_sqlalchemy(config)

    config.add_static_view(name='static', path='findex_gui:static')

    config.add_route('terms', '/terms')
    config.add_route('robots', '/robots.txt')
    config.add_route('favicon', '/favicon.ico')

    config.scan('findex_gui.views')

    config.include('findex_gui.themes.findex_official')

    return config.make_wsgi_app()
