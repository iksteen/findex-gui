def theme_static(request, path):
    return request.static_url('findex_gui:themes/findex_official/static/' + path)


def includeme(config):
    config.add_theme('findex_official')

    config.include('pyramid_jinja2')

    config.add_request_method(theme_static, 'theme_static')

    config.add_static_view(name='themes/findex_official', path='findex_gui:themes/findex_official/static')

    config.add_route('home', '/', theme='findex_official')
    config.add_route('search', '/search', theme='findex_official')
    config.add_route('api', '/api', theme='findex_official')
    config.add_route('research', '/research', theme='findex_official')
    config.add_route('research-mass-ftp-crawling', '/research/mass-ftp-crawling', theme='findex_official')
    config.add_route('documentation', '/documentation', theme='findex_official')

    config.scan('findex_gui.themes.findex_official.views')
