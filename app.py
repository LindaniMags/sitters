from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def create_app():
    """
    This function creates a new Flask application instance and
    configures it for use with the Sitters application.

    The application is configured to use a SQLite database at
    "sqlite:///testing.db", and is set up to use Flask-Login and
    Flask-Bcrypt.

    The function returns the new application instance.

    :return: A new Flask application instance
    :rtype: Flask
    """
    app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testing.db"
    app.secret_key="SOME KEY"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(uid):
        """
        The user loader function for Flask-Login.

        This function takes a user ID, and returns the associated User instance.

        :param uid: The user ID to load
        :type uid: int
        :return: The User instance associated with the given user ID
        :rtype: User
        """
        return User.query.get(uid)
    
    bcrypt = Bcrypt(app)

    from routes import register_routes
    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app