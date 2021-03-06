from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from flask_login import current_user, login_user, login_required
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3
from models.post import Post
from models.endorsement import Endorsement



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
        login_user(create_user)
        flash(f"Successfully created an account")
        return redirect(url_for('users.show', username=username))
    else:
        return render_template('users/new.html', errors=create_user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    user = User.get_or_none(User.username == username)
    # u = User.get_by_id(current_user.id) ## no need to use this
    if user:
        return render_template('users/show.html', user=user)
    else:
        return render_template('404.html')
    # if current_user.is_authenticated:
    #     return render_template('users/show.html', username=current_user.username, id=current_user.id)
    # else:
    #     flash(f"Please login to access profile page")
    #     return redirect(url_for('session.new'))


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    if current_user.is_authenticated:
        return render_template('users/edit.html', id=id, username=current_user.username, email=current_user.email, profile_image_url=current_user.profile_image_url)
    else:
        flash(f"Access not allowed, please login")
        return redirect(url_for('session.new'))


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)

    username_update = request.form.get('username_update')
    email_update = request.form.get('email_update')
    # breakpoint()
    if current_user == user:
        update_user = (User
                        .update(username=username_update,
                                email=email_update)
                        .where(User.id == user.id))
        update_user.execute()

        flash(f"Updated successfully")
        return redirect(url_for('users.show', username=current_user.username))
    else:
        flash(f"Unauthorized to perform this action. Login to continue")
        return redirect(url_for('session.new'))


# @users_blueprint.route('<id>/upload', methods=['POST'])
# def upload(id):
#     if profile_img_file not in request.files:
#         return "No profile_img_file key in request.files"

#     file = request.files["profile_img_file"]

#     if file.filename == "":
#         return 'Please select a file'

#     if file and allowed_file(file.filename):
#         file.filename = secure_filename(file.filename)
#         output = upload_file_to_s3(file, app.config.Config["S3_BUCKET"])
#         return str(output)

#     else:
#         flash(f"Could not upload the file to the database")
#         return redirect(url_for('home'))