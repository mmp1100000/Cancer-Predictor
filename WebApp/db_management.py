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
        return dict()
    else:
        models_dict = dict()
        for row in cancers_models:
            models_dict.setdefault(row[0], []).append(row[1])
        return models_dict


def get_models_html_selector():
    models = get_cancers_models()
    disease_options = ""
    model_options = ""
    for disease in models.keys():
        disease_options += '<option value="' + disease + '">' + disease + '</option>\n'
        model_options += '<optgroup data-rel="' + disease + '">\n'
        for model in models[disease]:
            model_options += '<option value="' + model + '">' + model + '</option>\n'
        model_options += '</optgroup>'

    return disease_options, model_options


def get_model(disease, model_type):
    conn = Connection()
    cancers_models = conn.do_query_mult_col(
        'SELECT model_path FROM model WHERE disease="' + disease + '" AND model_type="' + model_type + '";')
    return cancers_models[0]


def get_patient_from_db(id_patient):
    conn = Connection()
    uid = conn.do_query('SELECT id FROM patient WHERE patient_id="' + id_patient + '";')
    if uid is not None:
        return uid
    else:
        conn.do_query(
            'INSERT INTO patient(id_patient) VALUES (\'' + id_patient + '\');')
        conn.connection.commit()
        uid = conn.do_query('SELECT id FROM patient WHERE patient_id="' + id_patient + '";')
        print(uid)
        return uid


def insert_prediction(date, expression_file_path, result, model_id, patient_id, user_id):
    conn = Connection()
    conn.do_query(
        'INSERT INTO prediction(datetime, expression_file_path, result, model_id, patient_id, user_id)) VALUES (\'' + date + '\',\'' + expression_file_path + '\',\'' + result + '\',\'' + model_id + '\',\'' + patient_id + + '\',\'' + user_id + '\');')
    conn.connection.commit()
