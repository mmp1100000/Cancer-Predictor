import json

from mysql import connector
from mysql.connector import Error


class Connection:

    def __init__(self):
        try:
            json1_file = open('database/mysql_connection_settings.json')
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
