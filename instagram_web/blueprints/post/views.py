from flask import Blueprint, render_template, request, url_for, flash, redirect
from models.post import Post
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug.utils import secure_filename
from flask_login import current_user


post_blueprint = Blueprint('post',
                            __name__,
                            template_folder='templates')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@post_blueprint.route('/', methods=['POST'])
def create():
    if 'post_img_file' not in request.files:
        flash(f"No post_img_file key in request.files")
        return redirect(url_for('users.show', username=current_user.username))

    file = request.files["post_img_file"]

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file)

        if output:
            user = current_user.id
            image_path = output
            post = Post(user=user, image_path=image_path)
            post.save()
            flash(f"Image has been posted to your feed!")
            return redirect(url_for('users.show', username=current_user.username))

        else:
            flash(f"Could not upload the file to the database")
            return redirect(url_for('users.show', username=current_user.username))

    else:
        flash(f"File type not accepted, please try again")
        return redirect(url_for('users.show', username=current_user.username))