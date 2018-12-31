from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as SS
from flask import current_app as app
from bloggy import log_mngr, db
from flask_login import UserMixin

@log_mngr.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'def-profile.png')
    password = db.Column(db.String(60), nullable = False)
    posts = db.relationship('Posts', backref='author', lazy=True)
    comments = db.relationship('Comments', backref='author', lazy=True)
    todos = db.relationship('Todo', backref='author', lazy=True)
    def get_reset_token(self, expiration=1500):
        s = SS(app.config['SECRET_KEY'], expiration)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    @staticmethod
    def verify_token(token):
        s = SS(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    def __repr__(self):
        return(f"User('{self.username}' , '{self.email})' , '{self.image_file}'")

class Posts(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.String(10), nullable= False, default = datetime.now().strftime("%d-%m-%Y"))
    comments = db.relationship('Comments',cascade='all, delete', backref='post', lazy = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return(f"User('{self.title}' , '{self.content})' , '{self.date_posted}'")

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.Text(300), nullable = False)
    date_posted = db.Column(db.String(10), nullable= False, default = datetime.now().strftime("%d-%m-%Y"))
    time_posted = db.Column(db.String(10), nullable = False, default = datetime.now().strftime("%I:%M %p"))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return(f"User '{self.author.username}' , '{self.comment}' , '{self.date_posted}' , '{self.time_posted}'")


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    todo = db.Column(db.Text(600), nullable=False)
    time = db.Column(db.String(10), nullable = False, default = datetime.now().strftime("%I:%M %p"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    def __repr__(self):
        return( f"User{self.author.id}: todo -> '{self.todo}'" )
    
    
    
    
    
    
    
    
    