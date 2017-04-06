#!/usr/bin/env python

from datetime import datetime
import sys, getopt, ldap
from mysqlconnection import MySQLConnection
from ldapbind import LdapBind


def add_names():
    ids = []
    with MySQLConnection(autocommit=False) as select_cursor:
        select_cursor.execute("SELECT DISTINCT kaust_id FROM module_usage WHERE full_name = 'UNKNOWN'")
        row = select_cursor.fetchone()
        while row is not None:
            ids.append([str(c) for c in row])
            row = select_cursor.fetchone()

    with MySQLConnection() as insert_cursor:
        for id in ids:
            id = id[0]
            sql = """ UPDATE module_usage
                      SET full_name = %s
                      WHERE kaust_id = %s"""
            data = (get_full_name_from(id), id)
            print sql, data
            insert_cursor.execute(sql, data)

def get_full_name_from(kaust_id):
    with LdapBind() as l:
        try:
            searchFilter = "(uidNumber=%s)" % kaust_id
            results = l.search_ext_s('DC=KAUST,DC=EDU,DC=SA', ldap.SCOPE_SUBTREE, searchFilter, ['displayName'])
            # The results are {DN, ATRR} pairs returned as a list
            # Here's an example of the what's the output:
            # [('CN=arenaam,OU=STAFF,OU=KAUST USERS,DC=KAUST,DC=EDU,DC=SA', {'displayName': ['Antonio M. Arena']}),
            #  (None, ['ldap://DomainDnsZones.KAUST.EDU.SA/DC=DomainDnsZones,DC=KAUST,DC=EDU,DC=SA']),
            #  (None, ['ldap://ForestDnsZones.KAUST.EDU.SA/DC=ForestDnsZones,DC=KAUST,DC=EDU,DC=SA']),
            #  (None, ['ldap://KAUST.EDU.SA/CN=Configuration,DC=KAUST,DC=EDU,DC=SA'])]
            # That's why we have this masterpiece of code to pull out a user's real name :P
            return results[0][1]['displayName'][0]
        except Exception, error:
            print error
            return "UNKNOWN"

if __name__=='__main__':
    add_names()
