import pickle

from predictor.train_workbench import new_model, process_dataset

"""
This script is an example of how to create and save a Keras model to 
upload it to the web app.
"""

process_data = process_dataset('to_demo/colonTumor_train.arff', 'Class', 'positive', 'negative')
model = new_model(process_data['x'], process_data['y'], 2000)
with open('to_demo/colon_model.pkl', 'wb') as handle:
    pickle.dump(model, handle)
