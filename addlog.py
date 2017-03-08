#!/usr/bin/env python

from datetime import datetime
import mysql.connector
import sys, getopt, os, subprocess

def insert_data(kaust_id, mode, hostname, name, path):
    context = mysql.connector.connect(user='rcapps',
                                      password="rcapps",
                                      host='localhost',
                                      database='module_usage')
    cursor = context.cursor()
    now = datetime.now().date()
    insert = ("INSERT INTO module_usage "
              "(kaust_id, when, mode, hostname, name, path) "
              "VALUES (%(kaust_id)s, %(when)s, %(mode)s, %(hostname)s, %(name)s, %(path)s)")
    data = {
        'kaust_id': kaust_id,
        'when': now,
        'mode': mode,
        'hostname': hostname,
        'name': name,
        'path': path,
    }
    cursor.execute(insert, data)

    # Make sure data is committed to the database
    context.commit()
    cursor.close()
    context.close()

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
