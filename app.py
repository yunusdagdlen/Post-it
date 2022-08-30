from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid

from application import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
