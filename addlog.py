#!/usr/bin/env python

from datetime import datetime
import mysql.connector
import sys, getopt, os, subprocess, ldap
from mysqlconnection import MySQLConnection

def insert_data(kaust_id, mode, hostname, name, path):
    with MySQLConnection() as cursor:
        sql = ("INSERT INTO module_usage "
               "(kaust_id, full_name, when, mode, hostname, name, path) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        data = (kaust_id, get_full_name_from(kaust_id), datetime.now().date(), mode, hostname.lower(), name, path)
        cursor.execute(sql, data)

def get_full_name_from(kaust_id):
    l = ldap.initialize('ldap://wthdc1sr01.kaust.edu.sa')
    try:
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s('arenaam@KAUST.EDU.SA', 'blabla')
        searchFilter = "(uidNumber=%s)" % kaust_id
        return l.search_ext_s('DC=KAUST,DC=EDU,DC=SA', ldap.SCOPE_SUBTREE, searchFilter, ['displayName'])
    except Exception, error:
        print error
        return "UNKNOWN"
    finally:
        l.unbind_s()

def main(argv):
    mode = ''
    name = ''
    path = ''
    kaust_id = ''
    hostname = ''

    try:
        opts, args = getopt.getopt(argv, "hm:n:p:i:o:", ["mode=", "name=", "path=", "id=", "origin="])
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

if __name__=='__main__':
    main(sys.argv[1:])
