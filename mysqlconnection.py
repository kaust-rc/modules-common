import mysql.connector

class MySQLConnection(object):
    def __init__(self, user='apps', password='app5ar3thebesT', host='localhost',
                 database='env_modules', autocommit=True):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.autocommit = autocommit

    def __enter__(self):
        self.connection = mysql.connector.connect(user=self.user, password=self.password,
                                                  host=self.host, database=self.database,
                                                  autocommit=self.autocommit)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.autocommit:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()
        return
