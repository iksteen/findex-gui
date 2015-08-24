def theme_static(request, path):
    return request.static_url('findex_gui:themes/findex_official/static/' + path)


def includeme(config):
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('findex_gui:themes/findex_official/templates')

    config.add_request_method(theme_static, 'theme_static')

    config.add_static_view(name='theme', path='findex_gui:themes/findex_official/static')

    config.add_route('api', '/api')
    config.add_route('research', '/research')
    config.add_route('research-mass-ftp-crawling', '/research/mass-ftp-crawling')
    config.add_route('documentation', '/documentation')

    config.scan('findex_gui.themes.findex_official')
