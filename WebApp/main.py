from flask import Flask, jsonify, request, render_template

from login import user_validation

app = Flask(__name__, template_folder='template')


@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)


@app.route("/")
def hello():
    pass
    #return render_template('index.html')


@app.route('/login')
def login_page():
    # return app.send_static_file('/login/index.html')
    return render_template('index.html')


@app.route('/login-auth', methods=['POST'])
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
    app.run(debug=True)
