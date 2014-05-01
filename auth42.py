import base64
from ldap_server import LdapServer


class Auth42(LdapServer):
    """
    This class provides methods to interact with 42's ldap
    """

    def __init__(self):
        super(Auth42, self).__init__()

    def ldap_get_email(self, user):
        """
        Tries to get email for given user -> String
        """
        result = super(Auth42, self)._search_not_empty(user)
        if result is not None:
            alias = result.get("alias")[1]
            return alias

        return None

    def ldap_get_picture(self, user):
        """
        Tries to get picture of given user encoded in base64 -> String
        """
        result = super(Auth42, self)._search_not_empty(user)
        if result is not None:
            picture = result.get("picture")[0]
            return base64.b64encode(picture)

        return None

    def ldap_get_fullname(self, user):
        """
        Tries to get fullname of given user -> String
        """
        result = super(Auth42, self)._search_not_empty(user)
        if result is not None:
            fullname = (result.get("first-name")[0], result.get("last-name")[0])
            return ' '.join(str(name) for name in fullname)

        return None
