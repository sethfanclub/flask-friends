from friends import create_app

app = create_app()

if __name__ == '__main__':
  app.run(debug=True)
  
# Let users change their password
# Implement forgot password
# Let users message each other
# Make site responsive