import os
import time

from flask import Flask, escape, request, render_template, make_response, redirect, session, url_for
from flask import Markup
from werkzeug.utils import secure_filename

from data import generate_records_table, generate_table_from_db, hist_from_db
from db_management import update_user_rol, get_user_rol, delete_by_id, new_model, insert_new_user, \
    get_models_html_selector, get_json_values
from login import user_validation, user_registration
from predictor.train_workbench import evaluate_user_data

app = Flask(__name__, template_folder='template')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Needed for Flask Session management
app.config['DATA_TEST_DIR'] = 'testdata/'
app.config['MODEL_DATA_TEST_DIR'] = 'modeltestdata/'

predict_data=""

# ------ DOCTOR AND ANONYMOUS PREDICTOR -------
@app.route("/")  # predictor
def main_page():
    cancer_options, model_options = get_models_html_selector()
    if 'username' in session:  # If user already logged in

        if get_user_rol(session['username']) == 'Admin':
            return redirect('/administration')

        logout = Markup('<p class="nav-link text-warning" style="font-size: 160%">' + str(escape(session['username'])) + '</p> <a class="nav-link text-warning" href="/logout"  style="font-size: 160%">\
          <span class="glyphicon glyphicon-user"></span>\
          Log-out</a>')  # Logout HTML link
        nav = Markup(
            '<li class="nav-item active"> <a class ="nav-link text-warning active"  style=" font-weight: bold; '
            'font-size: 160%" href="" > '
            'Predictor </a></li><li class="nav-item"> <a class ="nav-link text-warning" style="font-size: '
            '160%" href="/records" > Records </a></li>')
        return make_response(
            render_template('index.html', navbar=nav, signin=logout,
                            cancer_options=Markup(cancer_options),
                               model_options=Markup(model_options),
                            results=Markup(predict_data)))  # Redirect to home, show logout link
    else:
        signin = Markup(' <a class="nav-link text-warning" href="/login"  style="font-size: 160%">\
                  <span class="glyphicon glyphicon-user"></span>\
                  Sign-in/Log-in</a>')  # If user not logged in, show login link
        anonymous_nav = Markup(
            '<li class="nav-item active"><a class ="nav-link text-warning active"  style="font-weight: bold; '
            'font-size: 160%" href="" > '
            'Predictor </a></li>')

        #requirements = generate_table_data_format(6)
        cancer_options, model_options = get_models_html_selector()
        return render_template('index.html', navbar=anonymous_nav,
                               signin=signin, #requirements=requirements,
                               cancer_options=Markup(cancer_options),
                               model_options=Markup(model_options),
                               results=Markup(predict_data)) # Redirect to home, show signin link if not logged in.


@app.route('/predictor', methods=['GET', 'POST'])
def predict():
    global predict_data
    if request.method == 'POST':
        file = request.files['file']
        cancer_type = request.form['disease']
        model_type = request.form['model']
        filename = time.strftime("%Y-%m-%d_%H%M%S") + secure_filename(file.filename)
        file.save(os.path.join(app.config['DATA_TEST_DIR'], filename))
        evaluate_user_data(session['username'], filename, cancer_type, model_type)
    return redirect('/')


# ------ DOCTOR RECORDS -------
@app.route("/records")
def records_page():
    rol = get_user_rol(session['username'])
    if 'username' not in session or rol != 'Doctor':
        return make_response(
            render_template('ERROR.html', error="Forbidden access"))  # Redirect to home, show logout link
    else:
        logout = Markup('<p class="nav-link text-warning" style="font-size: 160%">' + str(escape(session['username'])) + '</p> <a class="nav-link text-warning" href="/logout"  style="font-size: 160%">\
             <span class="glyphicon glyphicon-user"></span>\
              Log-out</a>')  # Logout HTML link
        table = generate_records_table(session['username'])
        return make_response(render_template('records.html', signin=logout,
                                             table=Markup(table)))  # Redirect to records, show logout link


# ------ ADMIN -------
@app.route("/statistics")
def admin_statistics_home():
    if get_user_rol(session['username']) == 'Admin':
        return redirect('/statistics/tables')
    else:
        return redirect('/')


@app.route("/statistics/<string:selected_content>")
def admin_statistics(selected_content):
    if 'username' not in session or get_user_rol(session['username']) != 'Admin':
        return make_response(
            render_template('ERROR.html'), error="Forbidden Access")  # Redirect to home, show logout link
    else:
        logout = Markup('<p class="nav-link text-warning" style="font-size: 160%">' + str(escape(session['username'])) + '</p> <a class="nav-link text-warning" href="/logout"  style="font-size: 160%">\
         <span class="glyphicon glyphicon-user"></span>\
          Log-out</a>')  # Logout HTML link

        if selected_content == 'tables':
            navigation = '<ul class="nav nav-tabs"><li class="nav-item"><a class="nav-link active" ' \
                         'href="/statistics/tables">Tables</a></li><li class="nav-item"><a class="nav-link" ' \
                         'href="/statistics/graphs">Graphs</a></li></ul>'
            content = generate_records_table(session['username'])
        elif selected_content == 'graphs':
            navigation = '<ul class="nav nav-tabs"><li class="nav-item"><a class="nav-link" ' \
                         'href="/statistics/tables">Tables</a></li><li class="nav-item"><a class="nav-link active" ' \
                         'href="/statistics/graphs">Graphs</a></li></ul>'
            content = hist_from_db()
        else:
            return make_response(
                render_template('ERROR.html', error="The selected_table or URL does not exist"))

        return make_response(
            render_template('statistics.html', content=Markup(content), navigation=Markup(navigation),
                            signin=logout))  # Redirect to admin, show logout link


@app.route("/administration")
def admin_administration_home():
    if get_user_rol(session['username']) == 'Admin':
        return redirect('/administration/user')
    else:
        return redirect('/')


@app.route("/administration/<string:selected_table>", methods=['GET'])
def admin_administration(selected_table):
    if 'username' not in session or get_user_rol(session['username']) != 'Admin':
        return redirect('/')
    else:
        logout = Markup('<p class="nav-link text-warning" style="font-size: 160%">' + str(escape(session['username'])) + '</p> <a class="nav-link text-warning" href="/logout"  style="font-size: 160%">\
         <span class="glyphicon glyphicon-user"></span>\
          Log-out</a>')  # Logout HTML link
        if selected_table == 'user':
            navigation = '<ul class="nav nav-tabs"><li class="nav-item"><a class="nav-link active" ' \
                         'href="/administration/user">Users</a></li><li class="nav-item"><a class="nav-link" ' \
                         'href="/administration/model">Models</a></li></ul>'
        elif selected_table == 'model':
            navigation = '<ul class="nav nav-tabs"><li class="nav-item"><a class="nav-link" ' \
                         'href="/administration/user">Users</a></li><li class="nav-item"><a class="nav-link active" ' \
                         'href="/administration/model">Models</a></li></ul>'
        else:
            return make_response(
                render_template('ERROR.html', error="The selected_table or URL does not exist"))
        table = generate_table_from_db(selected_table)
        return make_response(
            render_template('administration.html', navigation=Markup(navigation), selected_table=Markup(table),
                            signin=logout))  # Redirect to admin, show logout link


@app.route("/administration/user/edit", methods=['POST'])
def update_user():
    if get_user_rol(session['username']) == 'Admin':
        uid = request.form['uid']
        rol = request.form['rol']
        update_user_rol(uid, rol)
        return redirect('/')
    return make_response(
        render_template('ERROR.html', error="Forbidden access"))


@app.route("/get_model_info", methods=['POST'])
def get_model_info():
    res = request.form['res'].split(";")
    return Markup(get_json_values(res[0], res[1]))


@app.route("/administration/<string:selected_table>/delete/<int:uid>", methods=['GET'])
def delete_user(selected_table, uid):
    if get_user_rol(session['username']) == 'Admin':
        if delete_by_id(selected_table, uid):
            # It was possible to delete
            return redirect("/administration/" + selected_table)
        else:
            return make_response(
                render_template('ERROR.html', error="Invalid action: Cannot delete"))
    else:
        return make_response(render_template('ERROR.html', error="Forbidden access"))


@app.route("/administration/<string:selected_table>/insert", methods=['POST'])
def admin_insert(selected_table):
    if get_user_rol(session['username']) == 'Admin':
        if selected_table == 'user':
            new_user = request.form['username']
            new_password = request.form['password']
            new_email = request.form['email']
            rol = request.form['rol']
            insert_new_user(new_user, new_email, new_password, rol)
            return redirect('/')
        elif selected_table == 'model':
            disease = request.form['disease']
            model_type = request.form['model_type']
            dataset_description = request.files['dataset_description']
            model_path = request.files['model_path']
            test_data_path = request.files['test_data_path']
            filename = time.strftime("%Y-%m-%d_%H%M%S") + secure_filename(test_data_path.filename)
            test_data_path.save(os.path.join(app.config['MODEL_DATA_TEST_DIR'], filename))
            new_model(disease, model_type, dataset_description, model_path,
                      os.path.join(app.config['MODEL_DATA_TEST_DIR'], filename))
            return redirect('/administration/model')
    return make_response(
        render_template('ERROR.html', error="Forbidden access"))


# ------ USER MANAGEMENT -------
@app.route('/login')
def login_page():
    if 'username' in session:  # If user already logged in
        return redirect(url_for('main_page'))
    return render_template('login.html')  # Show login page


@app.route('/login-auth', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        if user_validation(user, password):  # If user in system
            session['username'] = user  # Set user session
            rol = get_user_rol(session['username'])
            if rol == "Doctor":
                return redirect(url_for('main_page'))
            elif rol == "Admin":
                return redirect('/administration/user')
        else:
            return make_response(
                render_template('login.html', message='Login error'))  # If user not in db, show login error
    else:
        return redirect(url_for('main_page'))


@app.route('/register-submit', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        if user_registration(firstname, lastname, email, request.form['password'],
                             request.form['repeated_password'], "Doctor"):  # If user registered sucessfully
            session['username'] = email  # Set user session
            if get_user_rol(session['username']) == "Doctor":
                return redirect(url_for('main_page'))
            elif get_user_rol(session['username']) == "Admin":
                return redirect('/administration/user')
        else:
            return make_response(
                render_template('register.html', error='Registration error'))

    return redirect(url_for('main_page'))


@app.route('/register')
def register_submit():
    if 'username' in session:  # If user already logged in
        return redirect(url_for('main_page'))
    else:
        return render_template('register.html')  # Show login page


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    app.run(debug=True)
