import base64
import ldap


class Auth42:
    """
    This class provides methods to interact with 42's ldap
    """

    _server_url = 'ldaps://ldap.42.fr'
    _base_dn = 'ou=paris,ou=people,dc=42,dc=fr'

    def __init__(self):
        self.server = self._new_connection()
        self.search = None

    @staticmethod
    def _new_connection():
        """
        Tries to connect with ldap server -> LDAPObject
        """
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        ldap.set_option(ldap.OPT_REFERRALS, ldap.OPT_OFF)
        try:
            return ldap.initialize(Auth42._server_url)
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
        if self.search is not None and self.search.get('login') == user: return self.search.get('data')

        data = self.server.search_s(self._base_dn, ldap.SCOPE_SUBTREE, '(uid=' + user + ')')

        if len(data): self.search = {'login': user, 'data': data[0][1]}
        else: self.search = None

        return self.search

    def ldap_get_email(self, user):
        """
        Tries to get email for given user -> String
        """
        result = self.ldap_search(user)
        if result is not None:
            alias = result.get('data').get('alias')
            return [m for m in alias if m == user + '@student.42.fr'][0]

        return None

    def ldap_get_fullname(self, user):
        """
        Tries to get fullname of given user -> String
        """
        result = self.ldap_search(user)
        if result is not None:
            return result.get('data').get('cn')[0]

        return None

    def ldap_get_number(self, user):
        """
        Tries to get the number of given user -> String
        """
        result = self.ldap_search(user)
        if result is not None:
            return result.get('data').get('mobile')[0]

        return None

    def ldap_authenticate(self, user, password, pool_month, pool_year):
        """
        Tries to authenticate user -> Boolean
        """
        student_info = ',ou=' + pool_month + ',ou=' + pool_year + ','
        dn = 'uid=' + user +  student_info + self._base_dn
        try:
            self.server.simple_bind_s(dn, password)
            return True
        except ldap.LDAPError:
            return False
