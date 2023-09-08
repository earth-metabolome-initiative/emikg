from flask_sqlalchemy import SQLAlchemy
# from flask_socketio import SocketIO, emit
from ..application import app

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
