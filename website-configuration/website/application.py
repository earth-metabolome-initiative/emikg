import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from alchemy_wrapper.database import DATABASE_URL

# from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder=os.path.abspath('static'))

# We set the session secret key for the application
app.secret_key = "hytrito8ew78ftoegfpdl"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy()
db.init_app(app)
with app.app_context():
    db.create_all()

# socketio = SocketIO(app)

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @socketio.on('update_data')
# def handle_update_data(data):
#     # Handle data updates here (e.g., process data)
#     # Send updated data to all connected clients
#     emit('data_updated', data, broadcast=True)
