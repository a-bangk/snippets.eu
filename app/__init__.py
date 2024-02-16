from flask import Flask
from dynaconf import FlaskDynaconf
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'login_bp.login'

def create_app():
    #This is a factory pattern
    app = Flask(__name__)
    FlaskDynaconf(
        app, 
        settings_files=["settings.toml", ".secrets.toml"]
    )
    with app.app_context():
        login.init_app(app)
        db.init_app(app)
        from . import source
        app.register_blueprint(source.source_bp)
        from . import author
        app.register_blueprint(author.author_bp)
        from . import tag
        app.register_blueprint(tag.tag_bp)
        from . import filter
        app.register_blueprint(filter.filter_bp)
        from . import about
        app.register_blueprint(about.about_bp)
        from . import home
        app.register_blueprint(home.home_bp)
        from . import write
        app.register_blueprint(write.write_bp)
        from . import authentication
        app.register_blueprint(authentication.login_bp)
        from . import error
        app.register_blueprint(error.error_bp)

        return app