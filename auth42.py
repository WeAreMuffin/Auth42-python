import base64
import ldap
from ldap_server import LdapServer


class Auth42(LdapServer):
    """
    This class provides methods to interact with 42's ldap
    """

    def __init__(self):
        super(Auth42, self).__init__()

    def ldap_authenticate(self, user, password):
        """
        Tries to authenticate user -> Boolean
        """
        dn = "uid=" + user + ",ou=2013,ou=people,dc=42,dc=fr"
        try:
            self.server.simple_bind_s(dn, password)
            response = True
        except ldap.LDAPError:
            response = False

        return response

    def ldap_search(self, user):
        """
        Tries to search for given user -> Dict
        """
        dn = "uid=" + user + ",ou=2013,ou=people,dc=42,dc=fr"
        try:
            return self.server.search_s(dn, ldap.SCOPE_SUBTREE)[0][1]
        except ldap.LDAPError:
            return None

    def ldap_get_email(self, user):
        """
        Tries to get email for given user -> String
        """
        result = self.ldap_search(user)
        if result is not None:
            alias = result.get("alias")[1]
            return alias
        
        return None

    def ldap_get_picture(self, user):
        """
        Tries to get picture of given user encoded in base64 -> String
        """
        result = self.ldap_search(user)
        if result is not None:
            picture = result.get("picture")[0]
            return base64.b64encode(picture)

        return None

    def ldap_get_fullname(self, user):
        """
        Tries to get fullname of given user -> String
        """
        result = self.ldap_search(user)
        if result is not None:
            fullname = (result.get("first-name")[0], result.get("last-name")[0])
            return ' '.join(str(name) for name in fullname)

        return None
