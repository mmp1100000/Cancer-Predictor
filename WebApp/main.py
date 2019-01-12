from flask import Flask, escape, request, render_template, make_response, redirect, session, url_for
from flask import Markup
from login import user_validation, user_registration, get_user_rol

app = Flask(__name__, template_folder='template')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Needed for Flask Session management


@app.route("/")  # predictor
def main_page():
    if 'username' in session:  # If user already logged in

        if get_user_rol(session['username']) == 'Admin':
            return make_response(
                render_template('ERROR.html', error="Forbidden access"))  # Redirect to home, show logout link

        logout = Markup('<p class="nav-link text-warning" style="font-size: 160%">' + str(escape(session['username'])) + '</p> <a class="nav-link text-warning" href="/logout"  style="font-size: 160%">\
          <span class="glyphicon glyphicon-user"></span>\
          Log-out</a>')  # Logout HTML link
        nav = Markup(
            '<li class="nav-item active"> <a class ="nav-link text-warning active"  style="font-size: 160%" href="" > '
            'Predictor </a></li><li class="nav-item"> <a class ="nav-link text-warning" style="font-size: '
            '160%" href="/records" > Records </a></li>')
        return make_response(
            render_template('index.html', navbar=nav, signin=logout))  # Redirect to home, show logout link
    else:
        signin = Markup(' <a class="nav-link text-warning" href="/login"  style="font-size: 160%">\
                  <span class="glyphicon glyphicon-user"></span>\
                  Sign-in/Log-in</a>')  # If user not logged in, show login link
        anonymous_nav = Markup(
            '<li class="nav-item active"><a class ="nav-link text-warning active"  style="font-size: 160%" href="" > '
            'Predictor </a></li>')
        return render_template('index.html', navbar=anonymous_nav,
                               signin=signin)  # Redirect to home, show signin link if not logged in.


@app.route("/admin")
def admin_page():

    if get_user_rol(session['username']) != 'Admin':
        return make_response(
            render_template('ERROR.html', error="Forbidden access"))  # Redirect to home, show logout link

    logout = Markup('<p class="nav-link text-warning" style="font-size: 160%">' + str(escape(session['username'])) + '</p> <a class="nav-link text-warning" href="/logout"  style="font-size: 160%">\
         <span class="glyphicon glyphicon-user"></span>\
          Log-out</a>')  # Logout HTML link
    nav = Markup('<li class="nav-item active"> <a class ="nav-link text-warning active"  style="font-size: 160%" '
                 'href="" > Administration </a></li>')
    return make_response(
        render_template('administration.html', navbar=nav, signin=logout))  # Redirect to admin, show logout link


@app.route("/records")
def records_page():

    if get_user_rol(session['username']) != 'Doctor':
        return make_response(
            render_template('ERROR.html', error="Forbidden access"))  # Redirect to home, show logout link

    logout = Markup('<p class="nav-link text-warning" style="font-size: 160%">' + str(escape(session['username'])) + '</p> <a class="nav-link text-warning" href="/logout"  style="font-size: 160%">\
             <span class="glyphicon glyphicon-user"></span>\
              Log-out</a>')  # Logout HTML link
    nav = Markup(
            '<li class="nav-item active"> <a class ="nav-link text-warning active"  style="font-size: 160%" href="/" > '
            'Predictor </a></li><li class="nav-item"> <a class ="nav-link text-warning" style="font-size: '
            '160%" href="/records" > Records </a></li>')
    return make_response(
        render_template('records.html', navbar=nav, signin=logout))  # Redirect to admin, show logout link


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
            if get_user_rol(session['username']) == "Doctor":
                return redirect(url_for('main_page'))
            elif get_user_rol(session['username']) == "Admin":
                return redirect(url_for('admin_page'))
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
                return redirect(url_for('admin_page'))
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
