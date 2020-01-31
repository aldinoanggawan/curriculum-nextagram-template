from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.post import Post
from flask_login import current_user, login_user, login_required
from app import gateway 
from models.endorsement import Endorsement

endorsement_blueprint = Blueprint('endorsement',
                                    __name__,
                                    template_folder='templates')

@endorsement_blueprint.route('/new/<post_id>', methods=['GET'])
def new(post_id):
    post = Post.get_by_id(post_id) #<object>
    client_token = gateway.client_token.generate()
    return render_template('endorsement/new.html', post=post, client_token=client_token)


@endorsement_blueprint.route('/<post_id>', methods=['POST'])
def create(post_id):
    amount = request.form.get('amount')
    nonce =  request.form.get('nonce')

    result = gateway.transaction.sale({
    "amount": amount,
    "payment_method_nonce": nonce,
    "options": {
      "submit_for_settlement": True
        }
    })

    if result.is_success:
        endorsement = Endorsement(amount=amount, post_id=post_id)
        endorsement.save()
        flash(f"Payment received, thank you for donating :)")
        return redirect('/')
    else:
        flash(f"An error occured, please try again later")
        return redirect('/')
