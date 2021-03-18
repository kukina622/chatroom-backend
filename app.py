from chat import createApp, socketio
from flask import Flask
import uuid


if __name__ == "__main__":
    app = Flask(__name__)
    app = createApp(app)
    app.config["SECRET_KEY"] = uuid.uuid4().hex
    app.debug = True    
    socketio.run(app)
