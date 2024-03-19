# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# # from flask_login import LoginManager
# from flask_login import LoginManager, login_user


# from flask import Flask
# from .extensions import db, bcrypt, login_manager
# from . import routes, models, forms
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.blueprints.routes import load_user
from .extensions import db, bcrypt, login_manager
import os

login_manager = LoginManager()

# Create Flask application instance
def create_app():
    app = Flask(__name__)
    
    # Configure Flask application
    app.config['SECRET_KEY'] = 'divinediv'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://myname:capstonepass@localhost/mybase'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # Set the login view name (route) for redirecting unauthenticated users
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.user_loader(load_user)
    from app.blueprints.routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    with app.app_context():
         db.create_all()
    return app
# # Initialize Flask extensions
# db = SQLAlchemy(app)
# from app import routes,models,forms
    
# login_manager = LoginManager(app)
# bcrypt = Bcrypt(app)


# login_manager.login_view = 'login'  # Set the login view name (route) for redirecting unauthenticated users
# login_manager.login_message = 'Please log in to access this page.'  
# #  Import views/routes (if not using blueprints)
# #from app import routes



# # Error handlers (optional)
# # @app.errorhandler(404)
# # def page_not_found(error):
# #     return render_template('404.html'), 404

