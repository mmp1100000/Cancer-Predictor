import pickle


def predict_leukemia(x, y):
    infile = open(
        '/Volumes/1TB HDD/Github projects/Cancer-Predictor/WebApp/predictor/models/leukemia-2019-01-15 11:22:51.997183.pkl',
        'rb')
    model = pickle.load(infile)
    infile.close()
    return model.evaluate(x, y, batch_size=128)
