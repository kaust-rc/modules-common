#!/usr/bin/env python

from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'env_modules'

TABLES = {}
TABLES['module_usage'] = (
    "CREATE TABLE `module_usage` ("
    "  `trans_id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `kaust_id` int(6) NOT NULL,"
    "  `full_name` varchar(50) NOT NULL,"
    "  `when` date NOT NULL,"
    "  `mode` varchar(10) NOT NULL,"
    "  `hostname` varchar(50) NOT NULL,"
    "  `name` varchar(20) NOT NULL,"
    "  `path` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`trans_id`),"
    "  KEY `kaust_id` (`kaust_id`),"
    "  CONSTRAINT `module_usage_ibfk_1` FOREIGN KEY (`kaust_id`) "
    "     REFERENCES `users` (`kaust_id`) ON DELETE CASCADE,"
    ") ENGINE=InnoDB")

context = mysql.connector.connect(user='rcapps', password='rcapps', host='localhost')
cursor = context.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    context.database = DB_NAME
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        context.database = DB_NAME
    else:
        print(err)
        exit(1)

for name, ddl in TABLES.iteritems():
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
context.close()
