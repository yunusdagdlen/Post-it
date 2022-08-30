from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # configure it in order -> prod overrides prp overrides dev
    app.config.from_pyfile('../config/dev.cfg', silent=True)
    app.config.from_pyfile('../config/prod.cfg', silent=False)

    # configure db
    db.app = app
    db.init_app(app)

    load_blueprints(app)

    return app


def load_blueprints(app):
    from application.controller import mod_pages
    from application.controllers.workspace_controller import mod_pages as workspace_module

    app.register_blueprint(mod_pages)