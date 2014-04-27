# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    auth42.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: aleger <aleger@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2014/04/27 23:45:26 by aleger            #+#    #+#              #
#    Updated: 2014/04/27 23:47:14 by aleger           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import ldap


def ldap_connect(user, password):
    """
    This function will try to connect user to 42's ldap server
    Return a boolean, False if authentication failed, True otherwise
    """

    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    ldap.set_option(ldap.OPT_REFERRALS, ldap.OPT_OFF)
    server = "ldaps://ldap.42.fr"
    connect = ldap.initialize(server)
    user_dn = "uid=" + user + ",ou=2013,ou=people,dc=42,dc=fr"
    try:
        connect.simple_bind_s(user_dn, password)
        response = True
    except ldap.LDAPError:
        response = False
    connect.unbind_s()
    return response
