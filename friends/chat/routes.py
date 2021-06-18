from . import events
from flask import Blueprint, render_template, request
from flask_login import login_required


chat = Blueprint('chat', __name__)

@chat.route('/chatroom', methods=['GET', 'POST'])
@login_required
def chatroom():
  return render_template('chatroom.html')