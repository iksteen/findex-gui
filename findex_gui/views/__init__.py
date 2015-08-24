from pyramid.view import view_config
from pyramid.response import Response, FileResponse
from pyramid.renderers import render_to_response
from findex_common import SearchException
import pkg_resources
from findex_gui.controllers.request import var_parse
from findex_gui.controllers.views.searcher import Searcher


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


@view_config(route_name='search', renderer='main/search.jinja2')
def search(request):
    search_vars = var_parse(request.params)
    message = ''

    if 'key' in search_vars:
        try:
            data = Searcher().search(request, search_vars)

            results = {-2: [], -1: [], 0: [], 1: [], 2: [], 3: [], 4: []}
            for f in data['results']['data']:
                if f.file_isdir:
                    results[-2].append(f)
                else:
                    results[f.file_format].append(f)

            results[-1] = data['results']['data']

            data['results']['data'] = results

            return render_to_response('main/search_results.jinja2', {'data': data, 'exception': None}, request=request)
        except SearchException as ex:
            message = str(ex)
        #except:
        #    message = 'Something went wrong \:D/'

    return {
        'message': message,
    }
