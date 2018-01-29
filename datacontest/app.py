from flask import Flask

from datacontest.rest import datathon, user
from datacontest.settings import DevConfig


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(user.blueprint)
    app.register_blueprint(datathon.blueprint)

    return app
