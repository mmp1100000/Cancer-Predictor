import hashlib
import json

from database.mysql_connector import Connection


def update_user_rol(uid, new_rol):
    """
    Updates rol in DB for given user.
    :param uid:
    :param new_rol:
    """
    conn = Connection()
    conn.do_query('UPDATE user SET rol=\"' + new_rol + '\" WHERE id=' + uid + ';')
    conn.connection.commit()


def get_user_rol(email):
    """
    Returns user rol from DB for given user
    :param email:
    :return: user rol (string)
    """
    conn = Connection()
    rol = conn.do_query('SELECT rol FROM user WHERE email=\"' + email + '\";')
    return rol[0]


def delete_by_id(table, uid):
    """
    Deletes user given its uid.
    :param table:
    :param uid:
    """
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
    """
    Inserts new user into DB
    :param username:
    :param email:
    :param password:
    :param rol:
    """
    input_password = hashlib.sha256(password.encode("utf8"))
    hex_dig = input_password.hexdigest()
    conn = Connection()
    conn.do_query(
        'INSERT INTO user(username, password, email, rol) VALUES (\'' + username + '\',\'' + hex_dig + '\',\'' + email + '\',\'' + rol + '\');')
    conn.connection.commit()


def new_model(disease, model_type, dataset_description, model_path, test_data_path):
    """
    Adds new model to DB
    :param disease:
    :param model_type:
    :param dataset_description:
    :param model_path:
    :param test_data_path:
    """
    from predictor.train_workbench import process_dataset, save_model
    description = json.loads(dataset_description.read().decode('utf8').replace("'", '"'))
    test_data = process_dataset(test_data_path,
                                description["class_info"]["name"],
                                description["class_info"]["values"][0],
                                description["class_info"]["values"][1])
    save_model(model_path, description, test_data['x'], test_data['y'], model_type, disease)


def get_cancers_models():
    """
    Returns disease and model type for each of the models in DB.
    :return: disease,model_type (dict).
    """
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
    """
    Returns html options for main page selector.
    :return: html string
    """
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


def get_model_path(disease, model_type):
    """
    Returns first DB occurrence of model filepath given a disease and a model type.
    :param disease:
    :param model_type:
    :return: model filepath (string)
    """
    conn = Connection()
    cancers_models = conn.do_query_mult_col(
        'SELECT model_path FROM model WHERE disease="' + disease + '" AND model_type="' + model_type + '";')
    return cancers_models[0]


def get_patient_from_db(id_patient):
    conn = Connection()
    uid = conn.do_query('SELECT id FROM patient WHERE patient_id="' + id_patient + '";')
    if uid:
        return uid[0]
    else:
        conn.do_query(
            'INSERT INTO patient(patient_id) VALUES (\'' + id_patient + '\');')
        conn.connection.commit()
        uid = conn.do_query('SELECT id FROM patient WHERE patient_id="' + id_patient + '";')
        print(uid)
        return uid[0]


def insert_prediction(date, expression_file_path, result, disease_name, model_name, patient_id, user_email):
    """
    Inserts new prediction query into DB.
    :param date:
    :param expression_file_path:
    :param result:
    :param disease_name:
    :param model_name:
    :param patient_id:
    :param user_email:
    """
    conn = Connection()
    model_id = conn.do_query('SELECT id from model WHERE model_type="' + model_name + '" AND disease="' + disease_name + '";')[0]
    patient_id = get_patient_from_db(patient_id)
    user_id = conn.do_query('SELECT id from user WHERE email="' + user_email + '";')[0]
    conn.do_query(
        'INSERT INTO prediction(datetime, expression_file_path, result, model_id, patient_id, user_id) VALUES (\'' + date + '\',\'' + expression_file_path + '\',\'' + result + '\',\'' + str(model_id) + '\',\'' + str(patient_id) + '\',\'' + str(user_id) + '\');')
    conn.connection.commit()


def get_json_values(disease, model_type):
    """
    Returns json model data in html table format for given disease and model type.
    :param disease:
    :param model_type:
    :return: html table (string)
    """
    conn = Connection()
    json_file = conn.do_query_mult_col(
        'SELECT dataset_description FROM model WHERE disease="' + disease + '" AND model_type="' + model_type + '";')[0]
    acc = get_model_acc(disease, model_type)
    with open('predictor/models/'+json_file[0]) as f:
        data = json.load(f)
        html= """<table class="table">
  <tbody>
    <tr>
      <th scope="row">Description</th>
      <td>"""+data['description']+"""</td>
    </tr>
    <tr>
      <th scope="row">Number of variables</th>
      <td>"""+str(data['num_of_variables'])+"""</td>
    </tr>
    <tr>
      <th scope="row">Class name</th>
      <td>"""+data['class_info']['name']+"""</td>
    </tr>
        <tr>
      <th scope="row">Class values</th>
      <td>"""+str(data['class_info']['values'])+"""</td>
    </tr>
    <tr>
      <th scope="row">Accuracy</th>
      <td>"""+str(acc[0])+"""</td>
    </tr>
  </tbody>
</table>"""
    return html


def get_model_acc(disease_name, model_name):
    """
    Returns model test ACC for given disease and model type.
    :param disease_name:
    :param model_name:
    :return: test ACC (list of string)
    """
    conn = Connection()
    model_id = \
    conn.do_query('SELECT id from model WHERE model_type="' + model_name + '" AND disease="' + disease_name + '";')[0]
    return conn.do_query('SELECT acc from model where id="' + str(model_id) + '";')