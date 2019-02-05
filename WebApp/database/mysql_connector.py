import json

from mysql import connector
from mysql.connector import Error


class Connection:
    """
    Creates a connection to the DB.
    do_query function can be used to do select queries.
    In order to do updates, drops or inserts, connection.commit() must
    be called.
    Connection params are to be obtained from json file.
    """

    def __init__(self, json_path='database/mysql_connection_settings.json'):
        try:
            json1_file = open(json_path)
            json1_str = json1_file.read()
            json1_data = json.loads(json1_str)
            self.host = json1_data['host']
            self.database = json1_data['database']
            self.port = json1_data['port']
            self.user = json1_data['user']
            self.password = json1_data['password']
        except Error as mysql_file_error:
            print(mysql_file_error)

        self.connection = connector.connect(host=self.host,
                                            database=self.database,
                                            port=self.port,
                                            user=self.user,
                                            password=self.password)

    def get_database(self):
        return self.database

    def do_query(self, query):
        print(query)
        res = list()
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            for result in cursor.fetchall():
                res.append(result[0])
            return res
        except Error as query_error:
            print(query_error)

    def do_query_mult_col(self, query):
        print(query)
        res = list()
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            for result in cursor.fetchall():
                res.append(result)
            return res
        except Error as query_error:
            print(query_error)
