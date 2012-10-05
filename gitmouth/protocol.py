from twisted.internet.protocol import Protocol
from twisted.python import log, failure
from twisted.internet.error import ProcessDone, ProcessTerminated
from twisted.internet.interfaces import IPushProducer
from zope.interface import implements

class ProcLiteProtocol(Protocol):
    implements(IPushProducer)

    def __init__(self):
        pass

    def connectionMade(self):
        pass

    def write(self, data):
        self.transport.write(data);

    def pair(self, clientProto):
        self.clientProto = clientProto

    def dataReceived(self, data):
        if str(data)[0:2] == 'E:':
            self.clientProto.errReceived(str(data)[2:])
        else:
            self.clientProto.write(data)

    def pauseProducing(self):
        self.transport.write('S:SIGSTOP\n');

    def resumeProducing(self):
        self.transport.write('S:SIGSTOP\n');

    def stopProducing(self):
        self.transport.write('S:SIGKILL\n');

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
