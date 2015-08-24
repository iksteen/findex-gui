from pyramid.view import view_config


@view_config(route_name='api', renderer='main/api.jinja2')
def api(request):
    return {}


@view_config(route_name='research', renderer='main/research.jinja2')
def research(request):
    return {}


@view_config(route_name='research-mass-ftp-crawling', renderer='main/research-mass-ftp-crawling.jinja2')
def research_mass_ftp_crawling(request):
    return {}


@view_config(route_name='documentation', renderer='main/documentation.jinja2')
def documentation(request):
    return {}
