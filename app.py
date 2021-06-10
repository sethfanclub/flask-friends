from friends import create_app

app = create_app()

if __name__ == '__main__':
  app.run(debug=True)
  
# Implement post form, settings form, comment form
# Let users delete comments, and edit posts
# Let users message each other
# Make site responsive
# Let users change their password