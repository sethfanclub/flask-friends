from flask_login import current_user
from flask_socketio import emit
from ..extensions import socketio


@socketio.on('message', namespace='/chatroom')
def handle_message(in_data):
	print(f"\ninside event: {current_user.is_authenticated}\n") # returns false
	sender_name = 'Seth'
	sender_pic_id = ''
	out_data = {
		'msg': f"{sender_name}: {in_data['msg']}",
		'pic_id': sender_pic_id
	}
	emit('message', out_data)