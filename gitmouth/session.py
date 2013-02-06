import base64
import re

from twisted.internet import reactor, defer, ssl
from twisted.python import log, failure
from twisted.conch.ssh import session
from twisted.conch import avatar
from zope.interface import implements
from twisted.web.client import Agent
from twisted.internet.error import ProcessTerminated
from twisted.web.http_headers import Headers
from twisted.internet.protocol import ClientCreator

from .protocol import ProcLiteProtocol, DumbProtocol
from .extractors import BuildServerExtractor

APP_NAME_RE = re.compile(r"^'/*(?P<app_name>[a-zA-Z0-9][a-zA-Z0-9@_-]*).git'$")


class OpenRukoSession(avatar.ConchUser):
    implements(session.ISession)

    def __init__(self, settings, api_key, key_fingerprint):
        avatar.ConchUser.__init__(self)
        self.agent = Agent(reactor)
        self.api_key = api_key
        self.key_fingerprint = key_fingerprint
        self.settings = settings
        self.channelLookup.update({'session': session.SSHSession})
        self.app_name_regex = APP_NAME_RE
        self.rez = None

    def execCommand(self, proto, cmd):

        proto.makeConnection(DumbProtocol())

        def return_path_error():
            proto.errReceived('\n ! Invalid path.')
            proto.errReceived('\n ! Syntax is: git@heroku.com:<app>.git where '
                              '<app> is your app\'s name.\n\n')
            reason = failure.Failure(ProcessTerminated(exitCode=1))
            return proto.processEnded(reason)

        if not cmd:
            return return_path_error()

        cmd_parts = cmd.split(' ')

        if len(cmd_parts) != 2:
            return return_path_error()

        app_command = cmd_parts[0]
        if app_command not in ['git-receive-pack', 'git-upload-pack']:
            return return_path_error()

        app_name_raw = cmd_parts[1]
        name_match = self.app_name_regex.match(app_name_raw)
        if name_match is None:
            return return_path_error()

        app_name = name_match.group('app_name')

        def buildProtoCallback(dyno_id):
            def setupProto(remoteProto):
                self.rez = remoteProto
                remoteProto.write(self.settings['apiserver_key'] + '\n')
                remoteProto.write(dyno_id + '\n')
                proto.makeConnection(remoteProto)
                remoteProto.pair(proto)
            return setupProto

        def connect_to_rez(rez_info):
            dyno_id = rez_info.get('dyno_id')
            cc = ClientCreator(reactor, ProcLiteProtocol)
            (cc.connectSSL(rez_info.get('host'),
                           self.settings['dynohost_rendezvous_port'],
                           ssl.ClientContextFactory()).
             addCallback(buildProtoCallback(dyno_id)))

        d = defer.Deferred()
        d.addCallback(connect_to_rez)

        def cbErrResponse(err):
            proto.errReceived('\n ! Unable to contact build server.\n\n')
            reason = failure.Failure(ProcessTerminated(exitCode=127))
            return proto.processEnded(reason)

        def cbResponse(resp):
            if resp.code == 200:
                resp.deliverBody(BuildServerExtractor(d))
            else:
                proto.errReceived('\n ! Unable to contact build server.\n\n')
                reason = failure.Failure(ProcessTerminated(exitCode=127))
                return proto.processEnded(reason)

        url = '%s://%s:%d/internal/%s/gitaction?command=%s' % (
            self.settings['apiserver_protocol'],
            self.settings['apiserver_hostname'],
            self.settings['apiserver_port'],
            app_name,
            app_command
        )
        auth_key = base64.b64encode(':%s' % self.settings['apiserver_key'])
        headers = Headers({'Authorization': [' Basic %s' % auth_key]})

        req = self.agent.request('POST', url, headers=headers)
        req.addCallback(cbResponse)
        req.addErrback(cbErrResponse)

        return

    def openShell(self, arg2):
        raise NotImplementedError

    def getPty(self, arg2, arg3, arg4):
        raise NotImplementedError

    def loseConnection(self):
        log.msg('lost connection')

    def eofReceived(self):
        log.msg('eof fired')

    def closed(self):
        log.msg('closed fired')
        if self.rez:
            self.rez.loseConnection()
