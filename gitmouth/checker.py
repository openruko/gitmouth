from twisted.conch.checkers import SSHPublicKeyDatabase
from twisted.internet import reactor, defer, error, ssl
from twisted.python import log
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.conch.ssh.keys import Key

import base64 

from extractors import UserExtractor

class OpenRukoCredentialChecker(SSHPublicKeyDatabase):

    agent = Agent(reactor) 

    def __init__(self, settings):
        self.settings = settings

    def checkKey(self, credentials):

         # dont bother checking until we've confirmed the key
         if not credentials.signature:
             return True

         cmp_key = Key.fromString(credentials.blob).fingerprint().replace(':','');

         apiserver_base_url = self.settings.get('apiserver_protocol') + '://' + self.settings.get('apiserver_hostname') + ':' + self.settings.get('apiserver_port') + '/'

         lookup_url = ( apiserver_base_url +
            'internal/lookupUserByPublicKey?fingerprint=' + cmp_key)

         log.msg("Checking fingerprint: " + lookup_url)

         d = defer.Deferred()

         def cbResponse(resp):
            if resp.code == 200:
                resp.deliverBody(UserExtractor(d, cmp_key, credentials))
            else:
                log.err('Key auth failed for ' + cmp_key)
                d.errback(False)

         def cbErrResponse(failure):
            log.err('Unable to contact api server')
            d.errback(False)

         req=self.agent.request('GET',lookup_url,
                 headers=Headers({ 'Authorization': [' Basic ' + 
                     base64.b64encode(':' + 
                         self.settings.get('apiserver_key'))]}))
         req.addCallback(cbResponse)
         req.addErrback(cbErrResponse)
         return d;

