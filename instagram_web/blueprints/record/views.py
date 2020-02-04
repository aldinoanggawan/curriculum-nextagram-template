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
        flash(f"You have sent a request to {following.username}")
        return redirect(url_for('users.show', username=following.username))
    else:
        flash(f"An error occured, please try again later")
        return redirect(url_for('users.show', username=following.username))


@record_blueprint.route('/<follower_id>/delete')
def destroy(follower_id):
    follower = User.get_by_id(follower_id)

    if current_user.unfollow(follower):
        flash(f"You have removed friend request from {follower.username}")
        return redirect(url_for('users.show', username=current_user.username))
    else:
        flash(f"An error occured, please try again later")
        return redirect(url_for('users.show', username=current_user.username))

@record_blueprint.route('/<following_id>/unfollow')
def unfollow(following_id):
    following = User.get_by_id(following_id)
    
    if current_user.unfollow(following):
        flash(f"You have unfollowed {following.username}")
        return redirect(url_for('users.show', username=following.username))
    else:
        flash(f"An error occured, please try again later")
        return redirect(url_for('users.show', username=following.username))