import ldap


class LdapServer(object):
    """
    Class used to connect/unconnect to ldap
    """

    _server_url = "ldaps://ldap.42.fr"
    _base_dn = ",ou=2013,ou=people,dc=42,dc=fr"

    def __init__(self):
        self.server = LdapServer._new_connection()
        self.search = None

    @staticmethod
    def _new_connection():
        """
        Tries to connect with ldap server -> LDAPObject
        """
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        ldap.set_option(ldap.OPT_REFERRALS, ldap.OPT_OFF)
        try:
            return ldap.initialize(LdapServer._server_url)
        except ldap.SERVER_DOWN:
            return None

    def close_connection(self):
        """
        Close connection with ldap server
        """
        self.server.unbind()

    def ldap_search(self, user):
        """
        Tries to search for given user -> Dict
        """
        dn = "uid=" + user + LdapServer._base_dn
        try:
            data = self.server.search_s(dn, ldap.SCOPE_SUBTREE)[0][1]
            self.search = {'login': user, 'data': data}
            return self.search
        except ldap.LDAPError:
            return None

    def _search_not_empty(self, user):
        """
        Return data for user if already exists or return a new search
        -> LDAPObject
        """
        if self.search is not None:
            if self.search.get("login") == user:
                return self.search.get("data")
        try:
            return self.ldap_search(user).get("data")
        except AttributeError:
            return None

    def ldap_authenticate(self, user, password):
        """
        Tries to authenticate user -> Boolean
        """
        dn = "uid=" + user + LdapServer._base_dn
        try:
            self.server.simple_bind_s(dn, password)
            response = True
        except ldap.LDAPError:
            response = False

        return response
