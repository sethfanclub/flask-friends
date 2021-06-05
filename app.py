from website import create_app

app = create_app()

if __name__ == '__main__':
  app.run(debug=True)

# Add user profile picture and cover art, and defaults for both