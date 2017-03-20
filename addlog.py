#!/usr/bin/env python

from datetime import datetime
import mysql.connector
import sys, getopt, os, subprocess, ldap

def insert_data(kaust_id, mode, hostname, name, path):
    context = mysql.connector.connect(user='apps',
                                      password="apps",
                                      host='localhost',
                                      database='env_modules',
                                      autocommit=True)
    try :
        with connection as cursor:
            sql = ("INSERT INTO module_usage "
                   "(kaust_id, full_name, when, mode, hostname, name, path) "
                   "VALUES (%(kaust_id)s, %(full_name)s, %(when)s, %(mode)s, %(hostname)s, %(name)s, %(path)s)")
            data = {
                'kaust_id': kaust_id,
                'full_name': get_full_name_from(kaust_id),
                'when': datetime.now().date(),
                'mode': mode,
                'hostname': hostname.lower(),
                'name': name,
                'path': path,
            }
            cursor.execute(sql, data)
            cursor.close()
    finally:
        # Close connection to database
        context.close()

def get_full_name_from(kaust_id):
    l = ldap.initialize('ldap://wthdc1sr01.kaust.edu.sa')
    try:
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s('arenaam@KAUST.EDU.SA', password)
        searchFilter = "(uidNumber=%s)" % kaust_id
        return l.search_ext_s('DC=KAUST,DC=EDU,DC=SA', ldap.SCOPE_SUBTREE, searchFilter, ['displayName'])
    except Exception, error:
        print error
    finally:
        l.unbind_s()

def main(argv):
    mode = ''
    name = ''
    path = ''
    kaust_id = ''
    hostname = ''

    try:
        opts, args = getopt.getopt(argv, "hm:n:p:i:hn:", ["mode=", "name=", "path=", "id=", "hostname="])
    except getopt.GetoptError:
        print 'write.modules.log.py -m <mode> -n <name> -p <path> -i <id> -hn <hostname>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'write.modules.log.py -m <mode> -n <name> -p <path> -i <id> -hn <hostname>'
            sys.exit(0)
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-i", "--id"):
            kaust_id = arg
        elif opt in ("-hn", "--hostname"):
            hostname = arg

    print 'KAUST ID is ', kaust_id
    print 'Host is ', hostname
    print 'Mode is ', mode
    print 'Name is ', name
    print 'Path is ', path
    insert_data(kaust_id, mode, hostname, name, path)

if __name__=='__main__':
    main(sys.argv[1:])
