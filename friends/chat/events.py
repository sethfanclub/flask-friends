from flask_socketio import emit
from ..extensions import socketio


@socketio.on('connect', namespace='/chatroom')
def test_connect():
	emit('after connect', {'data': 'Let\'s dance!'})