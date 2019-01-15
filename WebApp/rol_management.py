from database.mysql_connector import Connection
from login import conn


def update_user_rol(uid, new_rol):
    conn = Connection()
    conn.do_query('UPDATE user SET rol=\"' + new_rol + '\" WHERE id=' + uid + ';')
    conn.connection.commit()


def get_user_rol(email):
    rol = conn.do_query('SELECT rol FROM user WHERE email=\"' + email + '\";')
    return rol[0]