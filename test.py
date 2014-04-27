import sys
from auth42 import ldap_connect


if __name__ == "__main__":

    if len(sys.argv) == 3:
        user = sys.argv[1]
        password = sys.argv[2]
        if ldap_connect(user, password):
            print "Authentication success"
        else:
            print "Authentication error"
    else:
        print "Usage: python test.py <login> <password>"
