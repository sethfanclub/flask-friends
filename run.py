from website import create_app

app = create_app()

if __name__ == '__main__':
  app.run(debug=True)

# finish message flashing, make user profile