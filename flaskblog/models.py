from datetime import datetime
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin
from sqlalchemy import MetaData
from itsdangerous import URLSafeTimedSerializer





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    chats = db.relationship('Chat', backref='author', lazy=True)


    def get_reset_token(self, expires_sec=1800):  # Default expiration set to 30 minutes
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    @staticmethod
    def verify_reset_token(token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=1800)  # max_age ensures token expiration
        except Exception:
            return None  # Token expired or invalid
        user = User.query.get(data['user_id'])
        return user

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(200), nullable=True)  # Allow null images
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.relationship('Like', backref='post', lazy=True)


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.relationship('User', backref='comments', lazy=True)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)





# Create metadata specific to the Chat model
chat_metadata = MetaData()

class Chat(db.Model):
    __table_args__ = {'extend_existing': True, 'schema': None}
    __bind_key__ = None  # Ensure no binds are used
    
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    receiver = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, db.ForeignKey('user.id'), default=datetime.utcnow)
    image_file = db.Column(db.String(120), nullable=True)  # For image


Chat.__table__.metadata = chat_metadata

    #def __repr__(self):
        #return f"Chat('{self.message}', '{self.timestamp}')"






