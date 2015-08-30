from findex_gui.controllers.request import var_parse
from findex_gui.controllers.views.searcher import Searcher


def search(request):
    search_vars = var_parse(request.params)
    data = Searcher().search(request, search_vars)

    results = {-2: [], -1: [], 0: [], 1: [], 2: [], 3: [], 4: []}
    for f in data['results']['data']:
        if f.file_isdir:
            results[-2].append(f)
        else:
            results[f.file_format].append(f)

    results[-1] = data['results']['data']

    data['results']['data'] = results

    return data
