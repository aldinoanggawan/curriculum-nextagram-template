from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.session.views import session_blueprint
from instagram_web.blueprints.upload.views import upload_blueprint
from instagram_web.blueprints.post.views import post_blueprint
from instagram_web.blueprints.endorsement.views import endorsement_blueprint
from instagram_web.blueprints.record.views import record_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
import os
from instagram_web.util.google_oauth import oauth
import config

assets = Environment(app)
assets.register(bundles)

oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(session_blueprint, url_prefix="/session")
app.register_blueprint(upload_blueprint, url_prefix="/upload")
app.register_blueprint(post_blueprint, url_prefix="/post")
app.register_blueprint(endorsement_blueprint, url_prefix="/endorsement")
app.register_blueprint(record_blueprint, url_prefix="/record")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def home():
    return render_template('home.html')
