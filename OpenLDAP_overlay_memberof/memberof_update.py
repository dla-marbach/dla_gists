#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Skript zum Update der memberOf-Attribute
# Basierend auf:
# https://forge.univention.org/svn/dev/branches/ucs-4.2/ucs-4.2-0/management/univention-ldap-overlay-memberof/univention-update-memberof

###############################################################################

# Importieren allgemeiner Bibliotheken
import argparse, ldap, sys

###############################################################################

# Parsen der Programmparameter
parser = argparse.ArgumentParser(description='OpenLDAP Update memberOf')

# LDAP server
parser.add_argument('-s', dest='host', type=str, default='ldap://localhost:389', help='LDAP host (default: ldap://localhost:389')
# LDAP administrator
parser.add_argument('-u', dest='username', type=str, default='cn=Administrator,dc=dla-marbach,dc=de', help='Admin username (default: cn=Administrator,dc=dla-marbach,dc=de')
# LDAP admin password
parser.add_argument('-p', dest='password', type=str, help='Admin user password')

# Parsen
args = parser.parse_args()

###############################################################################

# Öffnen der Verbindung
l = ldap.initialize(args.host)

try:
    l.bind_s(args.username, args.password)

except ldap.INVALID_CREDENTIALS:
    print "Your username or password is incorrect."
    sys.exit()

except ldap.LDAPError, e:

    if type(e.message) == dict and e.message.has_key('desc'):
        print e.message['desc']
    else:
        print e

    sys.exit()

# Suchen aller Gruppen in group4beehive
results = l.search_s('ou=group4beehive,dc=dla-marbach,dc=de', ldap.SCOPE_SUBTREE, "(&(objectClass=groupOfNames)(member=*))", ["member"])

for result in results:
    dn = result[0]
    member = result[1].get("member", [""])

    if dn and member:

        try:
            # update groups
            ml = []
            ml.append((ldap.MOD_REPLACE, "member", member))
            l.modify_s(dn, ml)

        except Exception, e:
            sys.stderr.write("E: modifing %s failed error with %s\n" % (dn, e))
            sys.stderr.write("   please check the membership of this group\n")
            sys.exit(1)

l.unbind()
