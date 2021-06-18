from flask_migrate import current
from flask_socketio import emit, send
from flask_login import current_user
from ..extensions import socketio


@socketio.on('send message', namespace='/chatroom')
def handle_message(in_data):
	print(in_data)
	print(current_user.is_authenticated) # Why is this false?
	sender_name = 'Seth'
	sender_pic_id = ''
	out_data = {
		'msg': f"{sender_name}: {in_data['msg']}",
		'pic_id': ''
	}
	emit('message', out_data)