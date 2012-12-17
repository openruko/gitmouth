from twisted.internet.protocol import Protocol
from twisted.python import failure
from twisted.internet.error import ProcessDone


class ProcLiteProtocol(Protocol):

    def __init__(self):
        pass

    def connectionMade(self):
        pass

    def write(self, data):
        self.transport.write(data)

    def pair(self, clientProto):
        self.clientProto = clientProto

    def dataReceived(self, data):
        if str(data)[0:2] == 'E:':
            self.clientProto.errReceived(str(data)[2:])
        else:
            self.clientProto.write(data)

    def connectionLost(self, reason):
        self.clientProto.processEnded(failure.Failure(ProcessDone(0)))

    def loseConnection(self):
        self.transport.abortConnection()


class DumbProtocol(Protocol):

    def __init__(self):
        pass

    def connectionMade(self):
        pass

    def write(self, data):
        pass

    def pair(self, clientProto):
        pass

    def dataReceived(self, data):
        pass

    def connectionLost(self, reason):
        pass

    def loseConnection(self):
        pass
