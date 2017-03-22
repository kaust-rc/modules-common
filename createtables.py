#!/usr/bin/env python

from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
from mysqlconnection import MySQLConnection

TABLES = {}
TABLES['module_usage'] = (
    "CREATE TABLE IF NOT EXISTS module_usage ("
    "  trans_id int(11) NOT NULL AUTO_INCREMENT,"
    "  kaust_id int(6) NOT NULL,"
    "  full_name varchar(50) NOT NULL,"
    "  when date NOT NULL,"
    "  mode varchar(10) NOT NULL,"
    "  hostname varchar(50) NOT NULL,"
    "  name varchar(20) NOT NULL,"
    "  path varchar(100) NOT NULL,"
    "  PRIMARY KEY (trans_id),"
    "  KEY kaust_id (kaust_id),"
    ") ENGINE=InnoDB DEFAULT CHARSET=utf-8")

with MySQLConnection(user='apps', password='app5ar3thebesT', host='localhost', database='env_modules', autocommit=True) as cursor:
    for name, ddl in TABLES.iteritems():
        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists")
            else:
                print(err.msg)
        else:
            print("OK")
