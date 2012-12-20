import sys

from twisted.conch.ssh.factory import SSHFactory
from twisted.conch.ssh.keys import Key
from twisted.cred.portal import Portal
from twisted.python import log

from .realm import OpenRukoRealm
from .checker import OpenRukoCredentialChecker

log.startLogging(sys.stderr)


class OpenRukoSSHServer(SSHFactory):

    def __init__(self, settings):
        self.settings = settings
        self.portal = Portal(OpenRukoRealm(settings))
        self.portal.registerChecker(OpenRukoCredentialChecker(settings))
        self.privateKeys = {
            'ssh-rsa': Key.fromFile(settings['gitmouth_private_key']),
        }
        self.publicKeys = {
            'ssh-rsa': Key.fromFile(settings['gitmouth_public_key']),
        }
