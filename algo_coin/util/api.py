

class APIKey(object):
    def __init__(self, key, secret_key):
        """ """
        self.key = key
        self.secret_key = secret_key

    def get_key(self):
        """ """
        return self.key

    def get_secret_key(self):
        """ """
        return self.secret_key

    def __str__(self):
        """ """
        return self.key + "-" + self.secret_key

    def __repr__(self):
        """ """
        return self.__str__()
