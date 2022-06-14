from flask import url_for
from flask import Flask, render_template, request, make_response, session
from werkzeug.security import check_password_hash, generate_password_hash
import flask
from db_config import local_session
from db_files.db_repo import DbRepo

from tables.Users import Users

repo = DbRepo(local_session)
app = Flask(__name__)
app.secret_key = 'top secret'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


@app.route("/")
def home():
    try:
        if session['remember'] == 'on':
            return flask.redirect(url_for('login_success'))
    except:
        pass
    return flask.redirect(url_for('login'))


@app.route("/login", methods=["GET"])
def login():
    return render_template('login.html', try_again=False, registered_success=False)


@app.route('/my_app', methods=['GET'])
def login_success():
    try:
        if session['username'] is not None:
            user = repo.get_by_column_value(Users, Users.username, session['username'])
            if user[0] is not None:
                return render_template('my_app.html')
    except:
        pass
    return make_response('Could not verify', 401)


@app.route("/login_process", methods=["POST"])
def handel_login():
    form_data = request.form
    username = form_data.get('username')
    password = form_data.get('psw')
    print(request)
    print(form_data)
    try:
        user = repo.get_by_column_value(Users, Users.username, username)
        if username == user[0].username and check_password_hash(user[0].password, password):
            session['remember'] = request.form.get('remember')
            if session['remember'] == 'on':
                session['username'] = username
                session['pwd'] = password
            return flask.redirect(url_for('login_success'))
    except:
        pass
    return render_template('login.html', try_again=True)


@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template('signup.html', bad_repeat=False, pass_too_short=False, user_exists=False, email_exists=False)


@app.route("/signup_process", methods=['POST'])
def handle_signup():
    if request.form["psw"] != request.form["psw-repeat"]:
        return render_template('signup.html', bad_repeat=True)
    form_data = request.form
    username = form_data.get('username')
    password = form_data.get('psw')
    email = form_data.get('email')
    user_username = repo.get_by_column_value(Users, Users.username, username)
    user_email = repo.get_by_column_value(Users, Users.email, email)
    if user_username:
        return render_template('signup.html', bad_repeat=False, user_exists=True,
                               email_exists=False, pass_too_short=False, status=202, mimetype='application/json')
    elif user_email:
        return render_template('signup.html', bad_repeat=False, user_exists=False,
                               email_exists=True, pass_too_short=False, status=202, mimetype='application/json')
    elif len(password) < 6:
        return render_template('signup.html', bad_repeat=False, user_exists=False,
                               email_exists=False, pass_too_short=True, status=202, mimetype='application/json')
    else:
        repo.add(Users(username=username, password=generate_password_hash(password),
                       email=email, user_role=3))
        return render_template('login.html', try_again=False, registered_success=True,
                               status=201, mimetype='application/json')


# @app.route('/logout', methods=['GET'])
def logging_out():
    session['jwt'], session['remember'], session['username'], session['pwd'] = None, None, None, None
    return flask.redirect(url_for('login'))

app.run(debug=True, port=5431)
