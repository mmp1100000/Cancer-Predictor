import datetime
import pickle
import json
from keras.layers import Dense, Dropout
from keras.models import Sequential
from scipy.io import arff
import pandas as pd
import time
from leukemia_model import predict_leukemia

from database.mysql_connector import Connection


def process_dataset(train_filepath, test_filepath):
    data_train = arff.loadarff(train_filepath)
    data_test = arff.loadarff(test_filepath)

    df_train = pd.DataFrame(data_train[0])
    x_train = df_train.loc[:, df_train.columns != 'myclass']
    y_train = df_train['myclass']
    y_train = y_train.replace(b'AML', 0)
    y_train = y_train.replace(b'ALL', 1)

    df_test = pd.DataFrame(data_test[0])
    x_test = df_test.loc[:, df_test.columns != 'myclass']
    y_test = df_test['myclass']
    y_test = y_test.replace(b'AML', 0)
    y_test = y_test.replace(b'ALL', 1)
    return {'x_train': x_train, 'x_test': x_test, 'y_train': y_train, 'y_test': y_test}


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


def save_model(model, description, x_test, y_test, model_type='nnet'):
    conn = Connection('../database/mysql_connection_settings.json')
    model_name = 'leukemia-' + time.strftime("%Y-%m-%d_%H:%M:%S")
    outfile = open('models/' + model_name + '.pkl', 'wb')
    pickle.dump(model, outfile)
    outfile.close()
    model_info = {'model_name': model_name,
                  'model_description': description}

    json_path = model_name + '-model_info.json'
    with open('models/' + json_path, 'w') as f:
        json.dump(model_info, f)
    conn.do_query(
        'INSERT INTO model(train_date, acc, model_type, dataset_description, train_data_path) values (\"' + time.strftime(
            "%Y-%m-%d %H:%M:%S") + '\",\"' + str(
            round(evaluate_model(model, x_test, y_test)[
                      1], 3)) + '\",\"' + model_type + '\",\"' + json_path + '\",\"' + model_name + '\");')
    conn.connection.commit()


train_filepath = '/Volumes/1TB HDD/Github projects/Cancer-Predictor/WebApp/predictor/data/leukemia_train.arff'
test_filepath = '/Volumes/1TB HDD/Github projects/Cancer-Predictor/WebApp/predictor/data/leukemia_test.arff'

processed_data = process_dataset(train_filepath=train_filepath, test_filepath=test_filepath)

model = new_model(x_train=processed_data['x_train'], y_train=processed_data['y_train'])

save_model(model, 'Leukemia cancer predictor V1.', processed_data['x_test'], processed_data['y_test'])
