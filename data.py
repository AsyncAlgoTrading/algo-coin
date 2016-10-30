class DataBase(object):
    def __init__(self,  **data):
        for k, v in data:
            setattr(self, k, v)


class Match(DataBase):
    pass


class Received(DataBase):
    pass


class Open(DataBase):
    pass


class Done(DataBase):
    pass


class Change(DataBase):
    pass


class Error(DataBase):
    pass
