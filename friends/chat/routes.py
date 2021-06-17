from flask import Blueprint, render_template


chat = Blueprint('chat', __name__)

@chat.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
  return render_template('chatroom.html')