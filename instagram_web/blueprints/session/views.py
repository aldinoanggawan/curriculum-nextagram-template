from flask import Blueprint, render_template, request, url_for, flash
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
    #add the code to check if the user exist
    user = User.get(username = username)
    breakpoint()

    password_to_check = request.form.get('password')
    hashed_password = user.password
    # breakpoint()
    result = check_password_hash(hashed_password, password_to_check)

