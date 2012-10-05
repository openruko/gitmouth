from twisted.internet.protocol import Protocol
from twisted.python import log, failure
import json

class BuildServerExtractor(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.collected = ''

    def dataReceived(self, bytes):
        self.collected += bytes

    def connectionLost(self, reason):
        payload = json.loads(self.collected)
        self.finished.callback(payload)


class UserExtractor(Protocol):
    def __init__(self, finished, key_fingerprint, credentials):
        log.msg('data received')
        self.finished = finished
        self.credentials = credentials
        self.collected = ''
        self.key_fingerprint = key_fingerprint

    def dataReceived(self, bytes):
        log.msg('data received')
        self.collected += bytes

    def connectionLost(self, reason):
        parts=self.collected.split(':')
        self.credentials.username = parts[1] + ':' + self.key_fingerprint 
        self.finished.callback(True)
