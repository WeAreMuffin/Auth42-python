import base64
import datetime
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
            alias = result.get("alias")
            return [m for m in alias if m == user + "@student.42.fr"][0]

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

    def ldap_get_number(self, user):
        """
        Tries to get the number of given user -> String
        """
        result = super(Auth42, self)._search_not_empty(user)
        if result is not None:
            number = result.get("mobile-phone")[0]
            return number

        return None

    def ldap_get_birthdate(self, user):
        """
        Tries to get birthdate of giver user (format: Y-m-d) -> String
        """
        result = super(Auth42, self)._search_not_empty(user)
        if result is not None:
            dump = result.get("birth-date")[0]
            birthdate = datetime.datetime.strptime(dump[:8], '%Y%m%d')
            return str(birthdate)[:10]

        return None
