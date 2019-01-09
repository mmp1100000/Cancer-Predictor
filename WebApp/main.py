from flask import Flask, jsonify, request
from flask_login import LoginManager

from login import user_validation

login_manager = LoginManager()

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route('/login', methods=['POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    user = request.form['user']
    password = request.form['password']
    if user_validation(user, password):
        return jsonify({'response': 'OK'}), 201
    else:
        return jsonify({'response': 'login error'}), 201


if __name__ == '__main__':
    app.run()
