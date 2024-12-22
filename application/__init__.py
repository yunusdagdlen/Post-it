#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Post-it

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # configure it in order -> prod overrides prp overrides dev
    app.config.from_pyfile('../config/dev.cfg', silent=True)
    app.config.from_pyfile('../config/prp.cfg', silent=True)
    app.config.from_pyfile('../config/prod.cfg', silent=False)

    # configure db
    db.app = app
    db.init_app(app)

    # session secret key
    app.secret_key = '05586b38ce2dc8b4b4e74fa770006e4ed2eac64165dfb33474cbebdf067bbffa'

    # configure migrations
    migrate.init_app(app, db)

    load_blueprints(app)
    CORS(app)

    return app


def load_blueprints(app):
    from application.controller import mod_pages
    from application.controllers.workspace_controller import mod_pages as workspace_module
    from application.controllers.workspace_table_controller import mod_pages as workspace_table_module
    from application.controllers.note_controller import mod_pages as notes_module

    app.register_blueprint(mod_pages)
