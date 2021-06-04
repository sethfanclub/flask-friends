from website import create_app

app = create_app()

if __name__ == '__main__':
  app.run(debug=True)

# Design user, wall, and posts relationships
# make user profile