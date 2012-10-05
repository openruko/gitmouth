from twisted.conch.ssh.factory import SSHFactory
from twisted.conch.ssh.keys import Key
from twisted.cred.portal import Portal
from twisted.python import log

import sys

log.startLogging(sys.stderr)

from realm import OpenRukoRealm
from checker import OpenRukoCredentialChecker

class OpenRukoSSHServer(SSHFactory):


    def __init__(self, settings):
        self.settings = settings
        self.portal = Portal(OpenRukoRealm(settings))
        self.portal.registerChecker(OpenRukoCredentialChecker(settings))
        self.privateKeys = {'ssh-rsa': Key.fromFile(settings['private_key'])}
        self.publicKeys = {'ssh-rsa': Key.fromFile(settings['public_key'])}
