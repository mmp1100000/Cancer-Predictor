import json
import pickle
import time

import pandas as pd
from keras.layers import Dense, Dropout
from keras.models import Sequential
from scipy.io import arff

from database.mysql_connector import Connection
from db_management import get_model_path, insert_prediction


def process_dataset(filepath, class_name, class_val_0, class_val_1):
    data = arff.loadarff(filepath)

    df_train = pd.DataFrame(data[0])
    x = df_train.loc[:, df_train.columns != class_name]
    y = df_train[class_name].str.decode("utf-8")
    y = y.replace(class_val_0, 0)
    y = y.replace(class_val_1, 1)
    return {'x': x, 'y': y}


def new_model(x_train, y_train):
    model = Sequential()
    model.add(Dense(64, input_dim=7129, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    model.fit(x_train, y_train,
              epochs=20,
              batch_size=128)

    return model


def evaluate_model(model, x_test, y_test, batch_size=128):
    score = model.evaluate(x_test, y_test, batch_size)
    return score


def save_model(model, model_info, x_test, y_test, model_type, disease):
    conn = Connection('database/mysql_connection_settings.json')
    model_name = disease + time.strftime("%Y-%m-%d_%H%M%S")
    model.save('predictor/models/' + model_name)
    with open('predictor/models/' + model_name, 'rb') as f:
        model = pickle.load(f)
    json_path = model_name + '-model_info.json'
    with open('predictor/models/' + json_path, 'w') as f:
        json.dump(model_info, f)
    conn.do_query(
        'INSERT INTO model(train_date, acc, model_type,disease, dataset_description, model_path) values (\"' + time.strftime(
            "%Y-%m-%d_%H:%M:%S") + '\",\"' + str(
            round(evaluate_model(model, x_test, y_test)[
                      1],
                  3)) + '\",\"' + model_type + '\",\"' + disease + '\",\"' + json_path + '\",\"' + model_name + '\");')
    conn.connection.commit()


def evaluate_user_data(user_requesting, test_data_file_name, disease_name, model_name):
    model_path = 'predictor/models/'
    model_obj_path = model_path + get_model_path(disease_name, model_name)[0]
    print(model_obj_path)
    with open(model_obj_path + '-model_info.json') as data_file:
        data_json = json.load(data_file)
        num_of_variables = data_json['num_of_variables']

    extension = test_data_file_name.split('.')[-1]
    print(test_data_file_name)
    print(extension)
    if extension == 'arff':
        data = arff.loadarff('testdata/' + test_data_file_name)
        df_test = pd.DataFrame(data[0])
    elif extension == 'tsv':
        data = pd.DataFrame.from_csv('testdata/' + test_data_file_name, sep='\t', header=None)
        df_test = data.loc[:, 1:len(data.keys()) - 1]
        patients = list(data.index)
    if len(df_test.columns) != num_of_variables:
        print('error')
    with open(model_obj_path, "rb") as input_file:
        predictor = pickle.load(input_file)
    prediction = predictor.predict(df_test)
    prediction = pd.DataFrame(data=prediction, index=df_test.index, columns=['PREDICTION'])
    if user_requesting is not None:
        for index, row in prediction.iterrows():
            insert_prediction(time.strftime('%Y-%m-%d %H:%M:%S'), test_data_file_name, str(row[0]), disease_name,
                              model_name, str(index), user_requesting)
    print(prediction.to_html())
    return prediction.to_html()


def modify_result_table(table):
    res = "<div class = \"container\" style=\"margin-left: auto;margin-right: auto;\"> <table class=\"table " \
          "table-hover\"" + table
    res = res.split("<tr style=\"text-align: right;\">", 1)[0] + "<tr class=\"bg-info\" style=\"text-align: center;\">" + res.split("<tr style=\"text-align: right;\">", 1)[1]
    res = res.split("""<th></th>""", 1)[0] + "<th>PATIENT ID</th>" + res.split("""<th></th>""", 1)[1]
    res = res.split("""<tr>
      <th>0</th>
      <th></th>
    </tr>""")[0] + res.split("""<tr>
      <th>0</th>
      <th></th>
    </tr>""")[1]
    res += "<br> <br> <br> </div>"
    return res
