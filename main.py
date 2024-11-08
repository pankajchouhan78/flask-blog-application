from flask import Flask, redirect, url_for
import config
from db import db
from blog.routes import blog_blueprint
from flask_login import LoginManager, current_user
from blog.models import User


app = Flask(__name__)
app.config.from_object(config.Config)
app.secret_key = config.SECRET_KEY
app.config['LOGIN_VIEW'] = 'blog_blueprint.login'  # URL to redirect to if not logged in
db.init_app(app)

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database, based on user_id
    return User.query.get(int(user_id))
app.register_blueprint(blog_blueprint)


with app.app_context():
    db.create_all()
    
# Fallback route for unmatched URLs
@app.route('/<path:path>')
def fallback(path):
    # Redirect to the homepage (or any fallback URL)
    return redirect(url_for('blog_blueprint.index'))

if __name__ == '__main__':
    app.run(debug=True)
    # python3 main.py --port 5001

    
    
    





