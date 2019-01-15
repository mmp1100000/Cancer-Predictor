from flask import Flask, escape, request, render_template, make_response, redirect, session, url_for
from flask import Markup

from data import generate_records_table, generate_table_from_db, hist_from_db, delete_by_id
from rol_management import update_user_rol, get_user_rol
from login import user_validation, user_registration

app = Flask(__name__, template_folder='template')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Needed for Flask Session management


# ------ DOCTOR AND ANONYMOUS PREDICTOR -------
@app.route("/")  # predictor
def main_page():
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
            render_template('index.html', navbar=nav, signin=logout))  # Redirect to home, show logout link
    else:
        signin = Markup(' <a class="nav-link text-warning" href="/login"  style="font-size: 160%">\
                  <span class="glyphicon glyphicon-user"></span>\
                  Sign-in/Log-in</a>')  # If user not logged in, show login link
        anonymous_nav = Markup(
            '<li class="nav-item active"><a class ="nav-link text-warning active"  style="font-weight: bold; '
            'font-size: 160%" href="" > '
            'Predictor </a></li>')
        return render_template('index.html', navbar=anonymous_nav,
                               signin=signin)  # Redirect to home, show signin link if not logged in.


@app.route('/predictor')
def predict():
    pass


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
            render_template('ERROR.html'))  # Redirect to home, show logout link
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


@app.route("/administration/<string:selected_table>/delete/<int:uid>", methods=['GET'])
def delete_user(selected_table, uid):
    if get_user_rol(session['username']) == 'Admin':
        if delete_by_id(selected_table, uid):
            # It was possible to delete
            return redirect("/administration/"+selected_table)
        else:
            return make_response(
                render_template('ERROR.html', error="Invalid action: Cannot delete"))
    else:
        return make_response(render_template('ERROR.html', error="Forbidden access"))


@app.route("/administration/<string:selected_table>/insert", methods=['POST'])
def admin_insert(selected_table):
    print("llega")
    if get_user_rol(session['username']) == 'Admin':
        print(request)
        return redirect('/')
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
        rol = request.form['rol']
        if user_registration(firstname, lastname, email, request.form['password'],
                             rol):  # If user registered sucessfully
            session['username'] = email  # Set user session
            if get_user_rol(session['username']) == "Doctor":
                return redirect(url_for('main_page'))
            elif get_user_rol(session['username']) == "Admin":
                return redirect('/administration/user')
        else:
            return make_response(
                render_template('register.html', error='Registration error',
                                rols=Markup('<option>Doctor</option><option>Admin</option>')))

    return redirect(url_for('main_page'))


@app.route('/register')
def register_submit():
    if 'username' in session:  # If user already logged in
        return redirect(url_for('main_page'))
    else:
        return render_template('register.html',
                               rols=Markup('<option>Doctor</option><option>Admin</option>'))  # Show login page


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    app.run(debug=True)
