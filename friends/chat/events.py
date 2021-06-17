from flask_socketio import emit, send
from ..extensions import socketio


@socketio.on('connect', namespace='/chatroom')
def test_connect():
	emit('after connect', {'data': 'Let\'s dance!'})

@socketio.on('message', namespace='/chatroom')
def handle_message(msg):
	send(msg, broadcast=True)