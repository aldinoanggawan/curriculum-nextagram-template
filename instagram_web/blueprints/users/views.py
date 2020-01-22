from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User



users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username=request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    # hashed_pw = generate_password_hash(password)

    create_user = User(username=username, email=email, password=password)
    
    if create_user.save():
        flash(f"Successfully created an account. Continue sign in!")
        return redirect(url_for('users.new'))
    else:
        return render_template('users/new.html', errors=create_user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
