from database.mysql_connector import Connection


def update_user_rol(uid, new_rol):
    conn = Connection()
    conn.do_query('UPDATE user SET rol=\"' + new_rol + '\" WHERE id=' + uid + ';')
    conn.connection.commit()
