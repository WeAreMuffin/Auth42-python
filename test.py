import getpass
from auth42 import Auth42


if __name__ == "__main__":

    user = raw_input("Your login: ")
    password = getpass.getpass("Your password: ")
    ld = Auth42()
    if ld is not None:
        print "=========== Starting Tests ============"
        assert ld.ldap_authenticate(user, password) is not None

        print "\n\n=========== Testing valid search ==========="
        assert ld.ldap_search(user) is not None
        print "Success"

        print "\n\n=========== Testing invalid search ==========="
        assert ld.ldap_search("toto") is None
        print "Success"

        print "\n\n=========== Testing valid mail ==========="
        assert ld.ldap_get_email(user) == user + "@student.42.fr"
        print "Success"

        print "\n\n=========== Testing invalid mail ==========="
        assert ld.ldap_get_email("toto") is None
        print "Success"

        print "\n\n=========== Testing valid picture ==========="
        assert ld.ldap_get_picture(user) is not None
        print "Success"

        print "\n\n=========== Testing invalid picture ==========="
        assert ld.ldap_get_picture("toto") is None
        print "Success"

        print "\n\n=========== End of tests ============"
        ld.close_connection()
    else:
        print "Ldap server down, try again later\n"
