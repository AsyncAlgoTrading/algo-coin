from abc import ABCMeta, abstractmethod


class Callback(object):
    __meta__ = ABCMeta

    def __init__(self):
        pass

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
