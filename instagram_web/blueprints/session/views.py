from flask import Blueprint, render_template, request, url_for, flash, redirect, session
from models.user import User
from werkzeug.security import check_password_hash


session_blueprint = Blueprint('session',
                                __name__,
                                template_folder='templates')


@session_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('session/new.html')


@session_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    user = User.get_or_none(User.username == username)
    
    if user == None:
        flash(f"Wrong username")
        return redirect(url_for('session.new'))
    else:
        password_to_check = request.form.get('password')
        hashed_password = user.password
        result = check_password_hash(hashed_password, password_to_check)
        if result == True:
            session["user_id"] = user.id
            return redirect(url_for('home'))
        else :
            flash(f"Wrong password")
            return redirect(url_for('session.new'))

    
