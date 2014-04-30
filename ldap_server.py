import ldap


class LdapServer(object):
    """
    Class used to connect/unconnect to ldap
    """

    _server_url = "ldaps://ldap.42.fr"

    def __init__(self):
        self.server = LdapServer._new_connection()

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
        dn = "uid=" + user + ",ou=2013,ou=people,dc=42,dc=fr"
        try:
            return self.server.search_s(dn, ldap.SCOPE_SUBTREE)[0][1]
        except ldap.LDAPError:
            return None
