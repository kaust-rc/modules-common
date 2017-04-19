#!/usr/bin/env python

from datetime import datetime
import ldap
from mysqlconnection import MySQLConnection
from ldapbind import LdapBind


def insert_data(kaust_id, mode, hostname, name, path, ip_addr):
    insert_module_usage(kaust_id, mode, hostname, name, path)
    if is_loggable(hostname):
        insert_hostname_ip(hostname, ip_addr)

def insert_module_usage(kaust_id, mode, hostname, name, path):
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

def is_loggable(hostname):
    return not hostname.startswith('ca') and \
           not hostname.startswith('noor2-apps') and \
           not hostname.startswith('smp') and \
           not hostname.startswith('gpu') and \
           not hostname.startswith('rcfen') and \
           not hostname.startswith('smc-apps') and \
           not hostname.startswith('ci') and \
           not hostname.startswith('hkw') and \
           not hostname.startswith('csb')

def insert_hostname_ip(hostname, ip_addr):
    with MySQLConnection() as cursor:
        sql = "INSERT INTO hostname_ip(hostname, ip) VALUES(%s,%s) " \
              "ON DUPLICATE KEY UPDATE ip=%s"
        data = (hostname.lower(), ip_addr, ip_addr)
        cursor.execute(sql, data)
