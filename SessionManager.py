##############################################################################
#
# Copyright (C) Zenoss, Inc. 2016, all rights reserved.
#
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
#
##############################################################################

"""txsessionmgr - Client library for single persistent connections to a device.

Useful for situations when multiple connections to a device can be handled
with one connection through a single login, e.g. txciscoapic, txwinrm

"""

# Logging
import logging

from twisted.internet.defer import inlineCallbacks, returnValue

LOG = logging.getLogger('txsessionmgr')


class IClient(object):
    """
    Interface for Client
    """
    # used by SessionManager to uniquely identify the device
    key = None

    @inlineCallbacks
    def login(self):
        """
        Implement login procedure and return a token

        Token can be string, class instance, etc.
        """
        returnValue(None)

    @inlineCallbacks
    def logout(self):
        """
        Implement logout procedure and return None
        """
        returnValue(None)


class Session(object):
    """
    Session handler for connection to a device.

    deferred_init will kick off a deferred login to a device from the first
    client that needs the connection.  Subsequent clients will use the data
    returned from the first login.

    The Client class is responsible for implementing the login methods
    """
    def __init__(self):
        # Used to keep track of clients using session
        self._clients = set()

        # The currently valid token.  This can be anything that the client
        # needs to know the connection is alive
        self._token = None

        # Deferred waiting for login result.
        self._login_d = None

        # Error from last login if applicable.
        self._login_error = None

    @inlineCallbacks
    def deferred_init(self, client):
        """Return Deferred token."""
        self._clients.add(client)
        if self._token:
            returnValue(self._token)

        # No one already waiting for a token. Login to get a new one.
        if not self._login_d or self._login_d.called:
            self._login_d = self.client.login()

            try:
                self._token = yield self._login_d
            except Exception as e:
                self._login_error = e
                raise

        # At least one other client is already waiting for a token, and
        # the login to get it is already in progress. Wait for that
        # login to finish, then return its token.
        else:
            yield self._login_d
            if self._login_error:
                raise self._login_error

        returnValue(self._token)

    @inlineCallbacks
    def deferred_close(self, client):
        """Return Deferred None.

        Calls client.logout() only if all other clients using the same
        session have also called deferred_logout.

        """
        if len(self._clients) <= 1:
            if self._token:
                try:
                    yield self.client.logout()
                except Exception:
                    pass

            self._token = None

        if client in self._clients:
            self._clients.remove(client)
        returnValue(None)


class SessionManager(object):
    '''
    Class to manage open sessions to devices.
    '''
    def __init__(self):
        # Used to keep track of sessions
        # one per device
        self._sessions = {}

    def get_connection(self, key):
        return self._sessions.get(key, None)

    @inlineCallbacks
    def init_connection(self, client, session_class=Session):
        '''Initialize connection to device.
        If a session is already started return it.
        Else kick off deferred to initiate session
        '''
        session = self.get_connection(client.key)
        if session:
            returnValue(session._token)

        session = session_class()
        self._sessions[client.key] = session

        token = yield session.deferred_init(client)
        returnValue(token)

    @inlineCallbacks
    def close_connection(self, client):
        session = self.get_connection(client.key)
        if not session:
            returnValue(None)
        yield session.deferred_close(client)

    @inlineCallbacks
    def restart_connection(self, client):
        """
        TODO:
        """
        pass


SESSION_MANAGER = SessionManager()
