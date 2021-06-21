from os import name
from flask import session, request
from flask_login import current_user
from flask_socketio import emit, send, join_room
from ..extensions import socketio


@socketio.on('connect', namespace='/chatroom')
def on_connect():
	join_room('chatroom')
	emit('message', {'text': f"{current_user.screen_name} has connected"}, room='chatroom')

@socketio.on('send_message', namespace='/chatroom')
def send_message(text):
	emit('message', {'text': f"{current_user.screen_name}: {text}"}, room='chatroom')