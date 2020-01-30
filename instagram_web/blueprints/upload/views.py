from flask import Blueprint, render_template, request, url_for, flash, redirect
from models.user import User
from flask_login import login_user, login_required, logout_user, current_user
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename
from config import Config


upload_blueprint = Blueprint('upload',
                                __name__,
                                template_folder='templates')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_blueprint.route('/<id>', methods=['POST'])
def create(id):
    if 'profile_img_file' not in request.files:
        flash(f"No profile_img_file key in request.files")
        return redirect(url_for('users.edit'))

    file = request.files["profile_img_file"]

    if file.filename == "":
        flash(f"Please select a file")
        return redirect(url_for('users.edit', id=id))

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file)

        if output:
            print(output)
            User.update(profile_image_path=output).where(User.id==current_user.id).execute()
            flash(f"Upload successful")
            return redirect(url_for('users.edit', id=id))

        else:
            flash(f"Could not upload the file to the database")
            return redirect(url_for('users.edit', id=id))

    else:
        flash(f"File type not accepted, please try again")
        return redirect(url_for('users.edit', id=id))