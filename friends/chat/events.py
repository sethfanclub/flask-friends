from flask_socketio import send, emit
from ..extensions import socketio

@socketio.on('connect')
def test_connect():
	emit('after connect', {'data': 'Let\'s dance!'})