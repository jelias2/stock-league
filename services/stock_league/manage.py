import flask
from flask.cli import FlaskGroup

from app import app


flask_cli = FlaskGroup(app)


if __name__=='__main__':
    flask_cli()
