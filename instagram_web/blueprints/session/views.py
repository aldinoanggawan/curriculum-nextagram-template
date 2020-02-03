from flask import Blueprint, render_template, request, url_for, flash, redirect, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from instagram_web.util.google_oauth import oauth
from config import Config

session_blueprint = Blueprint('session',
                                __name__,
                                template_folder='templates')


@session_blueprint.route('/new', methods=['GET'])
def new():
    client_id = Config.GOOGLE_CLIENT_ID
    return render_template('session/new.html', client_id=client_id)


@session_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    user = User.get_or_none(User.username == username)
    
    if user:
        password_to_check = request.form.get('password')
        hashed_password = user.password
        result = check_password_hash(hashed_password, password_to_check)
        if result == True:
            # session["user_id"] = user.id # manage session manually
            login_user(user) # store user id in session
            return redirect(url_for('users.show', username=username))
        else :
            flash(f"Wrong password")
            return redirect(url_for('session.new'))       
    else:
        flash(f"Wrong username")
        return redirect(url_for('session.new'))


@session_blueprint.route('/delete')
@login_required
def destroy():
    logout_user()
    flash(f"You have successfully logged out")
    return redirect(url_for('home'))


@session_blueprint.route('/google_login')
def google_login():
    redirect_uri = url_for('session.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@session_blueprint.route('/authorize/google')
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)

    if user:
        login_user(user)
        flash(f"You have successfully logged in")
        return redirect('/')
    else:
        flash(f"Login failed, please create an account to proceed")
        return redirect(url_for('session.new'))