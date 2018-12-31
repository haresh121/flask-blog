from PIL import Image
import random
import os
import secrets
from bloggy import mail,messenger
from flask import url_for
from bloggy.models import User
from flask_mail import Message
from flask import current_app as app

def sendresetemail(user):
    token = user.get_reset_token(300)
    msg = Message('password request reset mail', sender='noreply@demo.com', recipients=[user.email])
    msg.body =f'''
    to reset follow the link
    {url_for('users.reset_token', token=token, _external = True)}
        
        
        
    <h4>if u did not request for the password change please ignore this message</h4>
    '''
    mail.send(msg)
    
    
def save_file(img_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(img_file.filename)
    pic_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/user-pics', pic_fn)
    
    output_size = (125, 125)
    i = Image.open(img_file)
    i.thumbnail(output_size)
    i.save(picture_path)
    return pic_fn

def randgen():
    x = random.randrange(50001, 100000, 2)
    return x

def byNum(username,num):
    x = randgen()
    num = str(num)
    msg = 'your security code ' + username + ' for password reset is ' + str(x)
    messenger.send(num, msg)
    su = User.query.filter_by(username=username).first()
    userdict = {
        'userid': su.username,
        'phno': num,
        'code': x
    }
    return userdict
    




















