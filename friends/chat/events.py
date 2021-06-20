from flask import session, request
from flask_login import current_user
from flask_socketio import emit
from ..extensions import socketio


@socketio.on('connect')
def test_connect():
	print(request.cookies.get('session'))
	emit('message', {'msg': 'User has connected'})

@socketio.on('message', namespace='/chatroom')
def handle_message(in_data):
	sender_name = 'Seth'
	sender_pic_id = ''
	out_data = {
		'msg': f"{sender_name}: {in_data['msg']}",
		'pic_id': sender_pic_id
	}
	emit('message', out_data)