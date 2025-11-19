from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from pythonic.config import Config
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

def create_app(class_config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from pythonic.main.routes import main
    from pythonic.users.routes import users
    from pythonic.admin.routes import admin

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(admin)

    return app
