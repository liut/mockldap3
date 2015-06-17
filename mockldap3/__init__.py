# -*- coding: utf-8 -*-

def mock_ldap():
    import sys
    import ldap3

    sys.modules['ldap3'].Server = Server
    sys.modules['ldap3'].Connection = Connection

class Server:
    users = {'user':dict( \
        pw="password", dn="user", uid='user', \
        cn='Eagle', sn='Liut', displayName='Dustman', \
        mail='dust@liut.cc' \
        )}

    def __init__(self, url):
        self.url = url

DefaultServer = Server('ldap://localhost')

class Connection:
    def __init__(self, server, **kw):
        print 'Connection init %r: %r' % (server, kw)
        self.server = server or DefaultServer
        self.user = kw.get('user')
        self.password = kw.get('password')
        if 'auto_bind' in kw and kw['auto_bind']:
            self.bind()

    def open(self):
        print 'Connection open'
        pass

    def bind(self):
        print 'Connection bind'
        if self.user == 'user' and self.password == 'password':
            return True
        user = self.server.users.get(self.user)
        if user is None:
            self.result = "Bind failed, user not found"
            return False
        if self.password == '' or user['pw'] == self.password:
            return True
        self.result = "Bind failed, invalid credentials"
        return False

    def search(self, search_base, search_filter, search_scope, attributes):
        print 'Connection search base: %s, filter: %s, scope: %s, attr: %s' % (search_base, search_filter, search_scope, attributes)
        # We have some hariness here to simulate the handling for openLDAP
        # servers that dont return dn as an attribute which we also do in
        # LDAP._search() in devpi_ldap/main.py
        class dnplaceholder(object):
            triggered = False

        def fixDn(user, k):
            if k in ('dn', 'distinguishedName'):
                dnplaceholder.triggered = k
                return dnplaceholder
            # else:
            #     raise KeyError(k)

        user = self.server.users.get('user')
        if user is not None:
            print user
            self.response = [dict(dn=user.get('dn'),attributes=dict(
                (k, [user.get(k, fixDn(user, k))]) for k in attributes if fixDn(user, k) is not dnplaceholder and k in user))]
            if dnplaceholder.triggered:
                self.response[0][dnplaceholder.triggered] = '(objectClass=*)'
            print 'response %r' % self.response
            return True

        search_filter = search_filter.split(":")
        if search_filter[0] == 'user':
            user = self.server.users.get(search_filter[1])
            if user is not None:
                self.response = [dict(attributes=dict(
                    (k, [user.get(k, fixDn(user, k))]) for k in attributes if fixDn(user, k) is not dnplaceholder))]
                if dnplaceholder.triggered:
                    self.response[0][dnplaceholder.triggered] = search_filter[1]
                return True
        elif search_filter[0] == 'group':
            user = self.server.users.get(search_filter[1])
            if user is not None and 'groups' in user:
                self.response = [
                    dict(attributes=dict(
                        (k, [g[k]]) for k in attributes))
                    for g in user['groups']]
                return True
        self.result = "Search failed"
        return False


