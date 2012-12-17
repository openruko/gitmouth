from twisted.cred.portal import IRealm
from zope.interface import implements

from .session import OpenRukoSession


class OpenRukoRealm():
    implements(IRealm)

    def __init__(self, settings):
        self.settings = settings

    def requestAvatar(self, auth_payload, mind, *interfaces):
        api_key, key_fingerprint = auth_payload.split(':', 1)
        payload = (interfaces[0], OpenRukoSession(self.settings, api_key,
                                                  key_fingerprint), lambda: None)
        return payload
