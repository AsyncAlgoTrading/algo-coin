from abc import ABCMeta, abstractmethod


class Callback(metaclass=ABCMeta):
    '''callback interface'''
    @abstractmethod
    def onMatch(self, data):
        '''onMatch'''

    @abstractmethod
    def onReceived(self, data):
        '''onReceived'''

    @abstractmethod
    def onOpen(self, data):
        '''onOpen'''

    @abstractmethod
    def onDone(self, data):
        '''onDone'''

    @abstractmethod
    def onChange(self, data):
        '''onChange'''

    @abstractmethod
    def onError(self, data):
        '''onError'''

    @abstractmethod
    def onAnalyze(self, data):
        '''onError'''


class NullCallback(Callback):
    def __init__(self):
        pass

    def onMatch(self, data):
        pass

    def onReceived(self, data):
        pass

    def onOpen(self, data):
        pass

    def onDone(self, data):
        pass

    def onChange(self, data):
        pass

    def onError(self, data):
        pass

    def onAnalyze(self, data):
        pass


class Print(Callback):
    def __init__(self,
                 onMatch=True,
                 onReceived=True,
                 onOpen=True,
                 onDone=True,
                 onChange=True,
                 onError=True):

        if not onMatch:
            setattr(self, 'onMatch', False)
        if not onReceived:
            setattr(self, 'onReceived', False)
        if not onOpen:
            setattr(self, 'onOpen', False)
        if not onDone:
            setattr(self, 'onDone', False)
        if not onChange:
            setattr(self, 'onChange', False)
        if not onError:
            setattr(self, 'onError', False)

    def onMatch(self, data):
        print(data)

    def onReceived(self, data):
        print(data)

    def onOpen(self, data):
        print(data)

    def onDone(self, data):
        print(data)

    def onChange(self, data):
        print(data)

    def onError(self, data):
        print(data)

    def onAnalyze(self, data):
        print(self._actions)
