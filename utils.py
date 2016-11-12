from datetime import datetime


def create_pair(key, typ, default=None):
    def get(self):
        if hasattr(self, '__' + str(key)):
            return getattr(self, '__' + str(key))
        if default is not None and type(default) == typ:
            return default
        # print(key, typ, default)
        raise TypeError("%s is unset" % key)

    def set(self, val):
        if not isinstance(val, typ):
            raise TypeError("%s attribute must be set to an instance of %s"
                            % (key, typ))
        setattr(self, '__' + str(key), val)
    return property(get, set)


def config(cls):
    new_cls_dict = {}
    for k, v in cls.__dict__.items():
        if isinstance(v, type):
            v = create_pair(k, v)
        elif isinstance(v, tuple) and \
                isinstance(v[0], type) and \
                isinstance(v[1], v[0]):
            v = create_pair(k, v[0], v[1])
        new_cls_dict[k] = v
    return type(cls)(cls.__name__, cls.__bases__, new_cls_dict)


def __init__(self, **kwargs):
    for item in self._svars:
        if item not in kwargs:
            print('WARNING %s unset!', item)
        else:
            setattr(self, item, kwargs.get(item))


def struct(cls):
    new_cls_dict = {}
    vars = []
    for k, v in cls.__dict__.items():
        if isinstance(v, type):
            v = create_pair(k, v)
            vars.append(k)

        new_cls_dict[k] = v
    new_cls_dict['__init__'] = __init__
    new_cls_dict['_vars'] = vars
    return type(cls)(cls.__name__, cls.__bases__, new_cls_dict)


def parseDate(date):
    try:
        date = datetime.fromtimestamp(float(date))
    except ValueError:
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date
