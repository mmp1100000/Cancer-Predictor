from _mysql import Error

import mysql.connector


class Connection:
    def __init__(self, host, database, port, user, password):
        try:
            self.connection = mysql.connector.connect(host=host,
                                                      database=database,
                                                      port=port,
                                                      user=user,
                                                      password=password)
        except Error as connection_error:
            print(connection_error)

    def do_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            for result in cursor.fetchall():
                print(result)
        except Error as query_error:
            print(query_error)
