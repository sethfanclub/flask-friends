from friends import create_app
from friends.extensions import socketio

app = create_app()

if __name__ == '__main__':
  socketio.run(app)

# finish chat
# Let users post pictures
# Let users message each other
# Make site responsive