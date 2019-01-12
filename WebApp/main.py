from flask import Flask, escape, request, render_template, make_response, redirect, session, url_for
from flask import Markup
from login import user_validation, user_registration

app = Flask(__name__, template_folder='template')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Needed for Flask Session management


@app.route("/")
def main_page():
    signin = Markup(' <a class="nav-link text-warning" href="/login"  style="font-size: 160%">\
          <span class="glyphicon glyphicon-user"></span>\
          Sign-in/Log-in</a>')  # If user not logged in, show login link

    if 'username' in session:  # If user already logged in
        logout = Markup('<p class="nav-link text-warning" style="font-size: 160%">' + str(escape(session['username'])) + '</p> <a class="nav-link text-warning" href="/logout"  style="font-size: 160%">\
          <span class="glyphicon glyphicon-user"></span>\
          Log-out</a>')  # Logout HTML link
        return make_response(render_template('index.html', signin=logout))  # Redirect to home, show logout link
    return render_template('index.html', signin=signin)  # Redirect to home, show signin link if not logged in.


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
            return redirect(url_for('main_page'))
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
        else:
            return make_response(
                render_template('register.html', error='Registration error', rols=Markup('<option>Doctor</option>')))

    return redirect(url_for('main_page'))


@app.route('/register')
def register_submit():
    if 'username' in session:  # If user already logged in
        return redirect(url_for('main_page'))
    else:
        return render_template('register.html', rols=Markup('<option>Doctor</option>'))  # Show login page


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    app.run(debug=True)
