#!/usr/bin/env python

from datetime import datetime
import sys
import getopt
import ldap
from mysqlconnection import MySQLConnection
from ldapbind import LdapBind


def insert_data(kaust_id, mode, hostname, name, path):
    with MySQLConnection() as cursor:
        sql = "INSERT INTO module_usage(kaust_id, full_name, when_date, mode, hostname, name, path) " \
              "VALUES(%s,%s,%s,%s,%s,%s,%s)"
        data = (kaust_id, get_full_name_from(kaust_id), datetime.now().date(), mode, hostname.lower(), name, path)
        cursor.execute(sql, data)

def get_full_name_from(kaust_id):
    with LdapBind() as ldap_bind:
        try:
            search_filter = "(uidNumber=%s)" % kaust_id
            results = ldap_bind.search_s('DC=KAUST,DC=EDU,DC=SA', ldap.SCOPE_SUBTREE, search_filter, ['displayName'])
            # The results are {DN, ATRR} pairs returned as a list
            # Here's an example of the what's the output:
            # [('CN=arenaam,OU=STAFF,OU=KAUST USERS,DC=KAUST,DC=EDU,DC=SA', {'displayName': ['Antonio M. Arena']}),
            #  (None, ['ldap://DomainDnsZones.KAUST.EDU.SA/DC=DomainDnsZones,DC=KAUST,DC=EDU,DC=SA']),
            #  (None, ['ldap://ForestDnsZones.KAUST.EDU.SA/DC=ForestDnsZones,DC=KAUST,DC=EDU,DC=SA']),
            #  (None, ['ldap://KAUST.EDU.SA/CN=Configuration,DC=KAUST,DC=EDU,DC=SA'])]
            # That's why we have this masterpiece of code to pull out a user's real name :P
            return results[0][1]['displayName'][0]
        except ldap.LDAPError, error:
            print error
            return "UNKNOWN"

def main(argv):
    mode = ''
    name = ''
    path = ''
    kaust_id = ''
    hostname = ''

    try:
        opts = getopt.getopt(argv, "hm:n:p:i:o:", ["mode=", "name=", "path=", "id=", "origin="])
    except getopt.GetoptError:
        print 'write.modules.log.py -m <mode> -n <name> -p <path> -i <id> -o <origin>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'write.modules.log.py -m <mode> -n <name> -p <path> -i <id> -o <origin>'
            sys.exit(0)
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-i", "--id"):
            kaust_id = arg
        elif opt in ("-o", "--origin"):
            hostname = arg

    print 'KAUST ID is ', kaust_id
    print 'Host is ', hostname
    print 'Mode is ', mode
    print 'Name is ', name
    print 'Path is ', path
    insert_data(kaust_id, mode, hostname, name, path)

if __name__ == '__main__':
    main(sys.argv[1:])
