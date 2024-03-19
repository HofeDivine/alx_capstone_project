# from flask_login import LoginManager
# login_manager = LoginManager(app)
# bcrypt = Bcrypt(app)


# login_manager.login_view = 'login'  # Set the login view name (route) for redirecting unauthenticated users
# login_manager.login_message = 'Please log in to access this page.'  
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
