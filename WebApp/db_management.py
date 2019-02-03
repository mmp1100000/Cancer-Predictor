import hashlib

from database.mysql_connector import Connection


def update_user_rol(uid, new_rol):
    conn = Connection()
    conn.do_query('UPDATE user SET rol=\"' + new_rol + '\" WHERE id=' + uid + ';')
    conn.connection.commit()


def get_user_rol(email):
    conn = Connection()
    rol = conn.do_query('SELECT rol FROM user WHERE email=\"' + email + '\";')
    return rol[0]


def delete_by_id(table, uid):
    conn = Connection()
    if table == "user" and len(conn.do_query('SELECT id FROM user WHERE rol=\"Admin\";')) == 1:
        # Invalid to delete last admin
        return False
    else:
        to_delete = conn.do_query('SELECT * FROM ' + table + ' WHERE id = \'' + str(uid) + '\';')
        if to_delete is not None:
            conn.do_query('DELETE FROM ' + table + ' WHERE id = \'' + str(uid) + '\';')
            conn.connection.commit()
            deleted = conn.do_query('SELECT * FROM ' + table + ';')
            return True
        else:
            return False


def insert_new_user(username, email, password, rol):
    input_password = hashlib.sha256(password.encode("utf8"))
    hex_dig = input_password.hexdigest()
    conn = Connection()
    conn.do_query(
        'INSERT INTO user(username, password, email, rol) VALUES (\'' + username + '\',\'' + hex_dig + '\',\'' + email + '\',\'' + rol + '\');')
    conn.connection.commit()


def new_model(disease, model_type, dataset_description, model_path, test_data_path):
    # test_data = process_dataset(test_data_path)
    print(type(dataset_description))
    print(type(model_path))
    print(type(test_data_path))
    # save_model(model_path, dataset_description, test_data['x'], test_data['y'], model_type)


def get_cancers_models():
    conn = Connection()
    cancers_models = conn.do_query_mult_col('SELECT disease, model_type FROM model;')
    if cancers_models is None:
        return ["No option available", "No option available"]
    else:
        # cancers = list()
        # models = list()
        # for row in cancers_models:
        #     cancers.append(row[0])
        #     models.append(row[1])
        # return [set(cancers), set(models)]
        res = list()
        for row in cancers_models:
            res.append(row[0] + " - " + row[1])
        return res
