import os
import config
from flask import Flask, render_template
from models.base_model import db
from models.user import User
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
import braintree

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.login_view = "session.new"
login_manager.login_message = u"Please login"
login_manager.init_app(app)


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get('BRAINTREE_MERCHANT_ID'),
        public_key=os.environ.get('BRAINTREE_PUBLIC_KEY'),
        private_key=os.environ.get('BRAINTREE_PRIVATE_KEY')
    )
)


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id) # get id from session,then retrieve user object from database with peewee query