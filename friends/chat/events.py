from flask import session, request
from flask.helpers import url_for
from flask_login import current_user
from flask_socketio import emit, send, join_room
from ..extensions import socketio


@socketio.on('connect', namespace='/chatroom')
def on_connect():
	join_room('chatroom')
	data = {
		'text': f"<b>{current_user.screen_name} has connected</b>",
		'imgURL': url_for('users.get_image', filename=f"{current_user.pic_id}")
		}
	emit('message', data, room='chatroom')

@socketio.on('send_message', namespace='/chatroom')
def send_message(text):
	data = {
		'text': f"{current_user.screen_name}: {text}",
		'imgURL': url_for('users.get_image', filename=f"{current_user.pic_id}")
		}
	emit('message', data, room='chatroom')