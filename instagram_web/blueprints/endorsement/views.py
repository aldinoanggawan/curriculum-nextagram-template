from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.post import Post
from flask_login import current_user, login_user, login_required

endorsement_blueprint = Blueprint('endorsement',
                                    __name__,
                                    template_folder='templates')

@endorsement_blueprint.route('/new/<post_id>', methods=['GET'])
def new(post_id):
    post = Post.get_by_id(post_id) #<object>
    return render_template('endorsement/new.html', post=post)