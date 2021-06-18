from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
import flask_login
from . import chat


@chat.route('/chatroom', methods=['GET', 'POST'])
@login_required
def chatroom():
  print(f"\ninside route: {current_user.is_authenticated}\n") # returns true
  if request.method == 'POST':
    return redirect(url_for('chat.chatroom'))
  return render_template('chatroom.html')