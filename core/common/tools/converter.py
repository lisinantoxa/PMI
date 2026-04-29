from collections import OrderedDict
from collections.abc import MutableMapping


class Converter(MutableMapping, OrderedDict):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Converter(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Converter(b) if isinstance(b, dict) else b)

    def __bool__(self):
        return len(self.__dict__.keys()) > 0

    def _obj_to_dict(self, value, _excluded_keys):
        _dict = {}
        for (k, value) in value.__dict__.items():
            if k in _excluded_keys:
                continue
            if isinstance(value, Converter):
                _dict.update({k: self._obj_to_dict(value, _excluded_keys)})
            elif isinstance(value, list):
                _dict.update({k: self._list_objs_to_list_dicts(value, _excluded_keys)})
            else:
                _dict.update({k: value})
        return _dict

    def __getitem__(self, item):
        if item in self.__dict__:
            return getattr(self, item)
        else:
            raise Exception(f'Not exist property {item}')

    def _list_objs_to_list_dicts(self, _list_objs, _excluded_keys):
        _list = []
        for i in _list_objs:
            if isinstance(i, Converter):
                _list.append(self._obj_to_dict(i, _excluded_keys))
            elif isinstance(i, list):
                _list.append(self._list_objs_to_list_dicts(i, _excluded_keys))
            else:
                _list.append(i)
        return _list

    def to_dict(self, excluded_keys=None):
        _excluded_keys = []
        if excluded_keys:
            _excluded_keys = [excluded_keys] if isinstance(excluded_keys, str) else excluded_keys
        return self._obj_to_dict(value=self, _excluded_keys=_excluded_keys)
