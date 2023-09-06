from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_socketio import SocketIO, emit

app = Flask(__name__)

# We set the session secret key for the application
app.secret_key = "hytrito8ew78ftoegfpdl"

# We connected to the PostgreSQL database using SQLAlchemy.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
db = SQLAlchemy(app)

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
