from pyramid.view import view_config
from pyramid.response import Response, FileResponse
import pkg_resources


@view_config(route_name='robots')
def beep_beep(request):
    return Response(
        body="User-agent: *\nDisallow: /browse/\nDisallow: /search\nDisallow: /goto/",
        content_type='text/plain',
        request=request,
    )


@view_config(route_name='favicon')
def favicon(request):
    icon = pkg_resources.resource_filename('findex_gui', 'static/img/favicon.ico')
    return FileResponse(icon, request=request)


@view_config(route_name='home', renderer='main/home.jinja2')
def home(request):
    return {}


@view_config(route_name='terms')
def terms(request):
    icon = pkg_resources.resource_filename('findex_gui', 'static/terms')
    return FileResponse(icon, content_type='text/plain', request=request)


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
