from uuid import uuid4

from flask import session
from flask.ext.bcrypt import Bcrypt
from flask.ext.openid import OpenID
from flask_oauth import OAuth
from flask.ext.login import LoginManager
from flask.ext.principal import Principal, Permission, RoleNeed


# Create the Flask-Bcrypt's instance
bcrypt = Bcrypt()
# Create the Flask-OpenID's instance
openid = OpenID()
# Create the Flask-OAuth's instance
oauth = OAuth()
# Create the Flask-Login's instance
login_manager = LoginManager()
# Create the Flask-Principal's instance
principals = Principal()

# Init the role permission via RoleNeed(Need).
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

# Setup the configuration for login manager.
#     1. Set the login page.
#     2. Set the more strong auth-protection.
#     3. Show the information when you are logging.
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"
# login_manager.anonymous_user = CustomAnonymousUser

# Create the auth object for facebook.
facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='1634926073468088',
    consumer_secret='a45ec6096ad272c4d61788b912a66394',
    request_token_params={'scope': 'email'})

twitter = oauth.remote_app(
    'twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='<TWITTER_APP_ID>',
    consumer_secret='<TWITTER_APP_SECRET>')


@openid.after_login
def create_or_login(resp):
    """Will be execute after pass the auth via openid."""

    from jmilkfansblog.models import db, User

    usernmae = resp.fullname or resp.nickname or resp.email
    if not username:
        flash('Invalid login. Please try again.', 'danger')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(username=usernmae).first()
    if user is None:
        user = User(id=str(uuid4()), username=username, password='jmilkfan')
        db.session.add(user)
        db.session.commit()

    # Logged in via OpenID.
    return redirect(url_for('blog.home'))


@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_oauth_token')


@twitter.tokengetter
def get_twitter_token():
    return session.get('twitter_oauth_token')


@login_manager.user_loader
def load_user(user_id):
    """Load the user's info."""

    from models import User
    return User.query.filter_by(id=user_id).first()
