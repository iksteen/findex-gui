from findex_common import SearchException
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from findex_gui.views import search as findex_search


@view_config(route_name='home', renderer='main/home.jinja2')
def home(request):
    return {}


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


@view_config(route_name='search', renderer='main/search.jinja2')
def search(request):
    if 'key' in request.params:
        try:
            results = findex_search(request)
            return render_to_response('main/search_results.jinja2', {'data': results, 'exception': None},
                                      request=request)
        except SearchException as ex:
            return {'message': str(ex)}
        except:
            return {'message': 'Something went wrong \:D/'}

    return {'message': ''}
