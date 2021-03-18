from flask import Flask, Blueprint
from flask_socketio import SocketIO
import uuid
from flask_login import LoginManager
from .Model.user import UserModel


socketio = SocketIO()
login_manager = LoginManager()


def createApp(app):

    socketio.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def user_loader(username):
        if not UserModel.is_exsit(username):
            return None

        user = UserModel()
        user.id = username
        return user

    from .api import api_bp
    from .Event import event_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(event_bp)
    return app
