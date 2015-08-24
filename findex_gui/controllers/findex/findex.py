from importlib import import_module

from sqlalchemy import and_

from findex_gui.db.orm import Files, Hosts
from findex_common.utils import DataObjectManipulation


class Findex(object):
    def __init__(self, db):
        self.db = db
        self._cache = {}

    def _get_cache(self, section, id):
        if not section in self._cache:
            return

        if id in self._cache[section]:
            return self._cache[section][id]

    def _set_cache(self, item):
        if isinstance(item, Hosts):
            k = 'hosts'
        elif isinstance(item, Files):
            k = 'files'
        else:
            return

        if not k in self._cache:
            self._cache[k] = {item.id: item}
        else:
            self._cache[k][item.id] = item

    def set_humanize(self, results):
        for f in results:
            f = DataObjectManipulation(f).humanize(humandates=True, humanpath=True, humansizes=True, dateformat="%d %b %Y")

            file_url = '%s%s' % (f.file_path_human, f.file_name_human)
            setattr(f, 'file_url', file_url)
        return results

    def set_icons(self, request, files):
        try:
            theme_icon_module = import_module('static.themes.%s.bin.icons' % request.theme_name)
            return theme_icon_module.set_icons(request=request, files=files)
        except Exception as ex:
            for f in files:
                f.img_icon = '/static/img/error.png'

        return files

    def get_host_objects(self, id=None):
        query = self.db.query(Hosts)

        cached = self._get_cache('hosts', id)
        if cached:
            return cached

        if isinstance(id, (int, long)):
            query = query.filter(Hosts.id == id)

        result = query.first()
        self._set_cache(result)

        return result

    def get_files_objects(self, id=None, host_id=None, file_path=None, total_count=None, offset=None):
        """
            total_count: number of results to fetch
            offset: the offset in db
        """
        query = self.db.query(Files)

        if id:
            _and = and_()
            _and.append(Files.id == id)
            query = query.filter(_and)
        elif isinstance(host_id, (int, long)):
            _and = and_()
            _and.append(Files.host_id == host_id)
            query = query.filter(_and)

        if isinstance(file_path, (str, unicode)):
            _and = and_()
            _and.append(Files.file_path == file_path)
            query = query.filter(_and)

        if isinstance(total_count, (long, int)):
            query = query.limit(total_count)
        
        results = query.all()

        if results:
            results = self.set_humanize(results)
            return results

        return []
