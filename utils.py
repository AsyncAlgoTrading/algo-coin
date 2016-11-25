import pytz
from datetime import datetime
from enums import ExchangeType


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
    for item in self._vars:
        if item not in kwargs:
            print('WARNING %s unset!', item)
        else:
            setattr(self, item, kwargs.get(item))


def __repr__(self):
    print(str(self.__class__))
    return '<' + ', '.join([x + '-' +
                           str(getattr(self, x))
                           if hasattr(self, '__' + x)
                           else x + '-' + 'UNSET'
                           for x in self._vars])
    + '>'


def struct(cls):
    new_cls_dict = {}
    vars = []
    for k, v in cls.__dict__.items():
        if isinstance(v, type):
            v = create_pair(k, v)
            vars.append(k)
        elif isinstance(v, tuple) and \
                isinstance(v[0], type) and \
                isinstance(v[1], v[0]):
            print('WARNING: no defaults in structs')
            v = create_pair(k, v[0])

        new_cls_dict[k] = v
    new_cls_dict['__init__'] = __init__
    new_cls_dict['__repr__'] = __repr__
    new_cls_dict['_vars'] = vars
    return type(cls)(cls.__name__, cls.__bases__, new_cls_dict)


def parse_date(date: str):
    try:
        date = datetime.utcfromtimestamp(float(date))
        date = pytz.utc.localize(date).astimezone(
            pytz.timezone('EST')).replace(tzinfo=None)
    except ValueError:
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date


def ex_type_to_ex(ex: ExchangeType):
    if ex == ExchangeType.GDAX:
        from exchanges.gdax import GDAXExchange
        return GDAXExchange
