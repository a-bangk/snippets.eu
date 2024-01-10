from flask import Flask
from dynaconf import FlaskDynaconf

def create_app():
    #This is a factory pattern
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'HGrsAtU^Bt7cV8D5'
    FlaskDynaconf(
        app, 
        settings_files=["settings.toml"]
    )
    with app.app_context():

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

        return app