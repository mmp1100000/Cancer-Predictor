import datetime
import pickle

from keras.layers import Dense, Dropout
from keras.models import Sequential
from scipy.io import arff
import pandas as pd

from leukemia_model import predict_leukemia

data_train = arff.loadarff(
    '/Volumes/1TB HDD/Github projects/Cancer-Predictor/WebApp/predictor/data/leukemia_train.arff')
data_test = arff.loadarff('/Volumes/1TB HDD/Github projects/Cancer-Predictor/WebApp/predictor/data/leukemia_test.arff')

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


def leukemia_model():
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
    #score = model.evaluate(x_test, y_test, batch_size=128)
    return model


#model = leukemia_model()

#outfile = open('models/leukemia-' + str(datetime.datetime.now()) + '.pkl', 'wb')
#pickle.dump(model, outfile)
#outfile.close()

print(predict_leukemia(x_test,y_test))