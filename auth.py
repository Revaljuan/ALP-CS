import os
from flask import Blueprint, url_for, redirect, session
from flask_jwt_extended import JWTManager, jwt_required as flask_jwt_required, create_access_token, get_jwt_identity
from models import User
from authlib.integrations.flask_client import OAuth

jwt = JWTManager()
oauth = OAuth()

# Initialize JWT
def init_jwt(app):
    jwt.init_app(app)

def create_access_token_local(identity):
    return create_access_token(identity=identity)

def jwt_required():
    return flask_jwt_required()

def current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)

# Initialize Google OAuth
def init_google(app):
    oauth.init_app(app)

    google = oauth.register(
        name='google',
        client_id=os.environ.get('GOOGLE_CLIENT_ID', 'YOUR_CLIENT_ID'),
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET', 'YOUR_CLIENT_SECRET'),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid email profile'}
    )

    bp = Blueprint('google', __name__)

    @bp.route('/login/google')
    def login_google():
        redirect_uri = url_for('google.authorize_google', _external=True)
        return google.authorize_redirect(redirect_uri)

    @bp.route('/authorize/google')
    def authorize_google():
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()
        session['user'] = user_info
        return redirect('/')

    return bp
