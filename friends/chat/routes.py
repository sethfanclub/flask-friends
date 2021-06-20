from flask import render_template, redirect, url_for, request, session
from flask_login import login_required, current_user
from . import chat


@chat.route('/chatroom', methods=['GET', 'POST'])
@login_required
def chatroom():
  if request.method == 'POST':
    return redirect(url_for('chat.chatroom'))
  return render_template('chatroom.html')