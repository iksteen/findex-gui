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


@view_config(route_name='terms')
def terms(request):
    icon = pkg_resources.resource_filename('findex_gui', 'static/terms')
    return FileResponse(icon, content_type='text/plain', request=request)

