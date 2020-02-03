from flask import Blueprint, render_template, request, url_for, flash, redirect
from werkzeug.utils import secure_filename
from flask_login import current_user
from models.user import User


record_blueprint = Blueprint('record',
                            __name__,
                            template_folder='templates')


@record_blueprint.route('/<following_id>')
def create(following_id):
    following = User.get_by_id(following_id)
    
    if current_user.follow(following):
        flash(f"You have followed {following.username}")
        return redirect(url_for('users.show', username=following.username))
    else:
        flash(f"An error occured, please try again later")
        return redirect(url_for('users.show', username=following.username))
        