from abc import ABCMeta, abstractmethod


class DataSource(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        self._callbacks = {'MATCH': [],
                           'RECEIVED': [],
                           'ERROR': [],
                           'OPEN': [],
                           'DONE': [],
                           'CHANGE': [],
                           'ANALYZE': []}

    def run(self, engine):
        try:
            while True:
                engine.tick()

        except KeyboardInterrupt:
            return

    @abstractmethod
    def onMatch(self, callback):
        '''onMatch'''

    @abstractmethod
    def onReceived(self, callback):
        '''onReceived'''

    @abstractmethod
    def onOpen(self, callback):
        '''onOpen'''

    @abstractmethod
    def onDone(self, callback):
        '''onDone'''

    @abstractmethod
    def onChange(self, callback):
        '''onChange'''

    @abstractmethod
    def onError(self, callback):
        '''onError'''

    @abstractmethod
    def registerCallback(self, callback):
        '''registerCallback'''
