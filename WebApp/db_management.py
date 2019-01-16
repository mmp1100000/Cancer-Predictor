from database.mysql_connector import Connection
from predictor.train_workbench import save_model, process_dataset


def update_user_rol(uid, new_rol):
    conn = Connection()
    conn.do_query('UPDATE user SET rol=\"' + new_rol + '\" WHERE id=' + uid + ';')
    conn.connection.commit()


def get_user_rol(email):
    conn = Connection()
    rol = conn.do_query('SELECT rol FROM user WHERE email=\"' + email + '\";')
    return rol[0]


def delete_by_id(table, uid):
    print(uid)
    conn = Connection()
    to_delete = conn.do_query('SELECT * FROM ' + table + ' WHERE id = \'' + str(uid) + '\';')
    print(to_delete)
    if to_delete is not None:
        conn.do_query('DELETE FROM ' + table + ' WHERE id = \'' + str(uid) + '\';')
        conn.connection.commit()
        deleted = conn.do_query('SELECT * FROM ' + table + ';')
        return True
    else:
        return False


def new_user(username, email, password, rol):
    conn = Connection()
    conn.do_query(
        'INSERT INTO user(username, password, email, rol) VALUES (\'' + username + '\',\'' + password + '\',\'' + email + '\',\'' + rol + '\');')

def new_model(disease, model_type, dataset_description, model_path, test_data_path):
    #test_data = process_dataset(test_data_path)
    print(type(dataset_description))
    print(type(model_path))
    print(type(test_data_path))
    #save_model(model_path, dataset_description, test_data['x'], test_data['y'], model_type)