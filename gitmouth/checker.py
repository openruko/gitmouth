import base64

from twisted.conch.checkers import SSHPublicKeyDatabase
from twisted.internet import reactor, defer
from twisted.python import log
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.conch.ssh.keys import Key

from .extractors import UserExtractor


class OpenRukoCredentialChecker(SSHPublicKeyDatabase):

    agent = Agent(reactor)

    def __init__(self, settings):
        self.settings = settings

    def checkKey(self, credentials):

        # dont bother checking until we've confirmed the key
        if not credentials.signature:
            return True

        cmp_key = Key.fromString(
            credentials.blob).fingerprint().replace(':', '')

        apiserver_base_url = '%s://%s:%d/' % (
            self.settings['apiserver_protocol'],
            self.settings['apiserver_hostname'],
            self.settings['apiserver_port']
        )

        lookup_url = '%sinternal/lookupUserByPublicKey?fingerprint=%s' % (
            apiserver_base_url ,cmp_key)

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

        auth_key = base64.b64encode(':%s' % self.settings['apiserver_key'])
        headers = Headers({'Authorization': [' Basic %s' % auth_key]})

        req = self.agent.request('GET', lookup_url, headers=headers)
        req.addCallback(cbResponse)
        req.addErrback(cbErrResponse)

        return d
