from flask import Blueprint
from flask import render_template,redirect, url_for, flash, request, abort
import secrets
from flask import current_app as app
from bloggy import db,bcrypt,messenger
from bloggy.users.forms import RegisterForm,LoginForm,ReqresetForm,ResetpassForm,UpdateForm,ReqnumForm, ReqresetnumForm
from bloggy.users.utils import sendresetemail, save_file, byNum
from bloggy.models import User
from flask_login import login_user,current_user,logout_user, login_required
from sqlalchemy.sql.expression import func,desc



users = Blueprint('users', __name__)


@users.route('/register', methods=['post', 'get'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        x = form.Password.data
        pass_hash = bcrypt.generate_password_hash(x).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = pass_hash)
        db.session.add(user)
        db.session.commit()
        flash(f'account created for user {form.username.data} now log in with your data!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, titles = '- Register')


@users.route('/login', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first_or_404()
        if user and bcrypt.check_password_hash( user.password, form.Password.data):
            login_user(user, remember = form.remember.data)
            flash('successully logged in!!', 'success')
            nextpg = request.args.get('next')
            return redirect(nextpg) if nextpg else redirect(url_for('main.home'))
        else:
            flash('please check email/password and enter', 'danger')
    return render_template('login.html', form=form,titles = '- Login')

@users.route('/account', methods=['post', 'get'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.pic.data:
            upic = save_file(form.pic.data)
            current_user.image_file = upic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('account updated successfully', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    prof_img = url_for('static',filename='user-pics/'+current_user.image_file)
    return render_template('about.html', titles = '- About',form = form, prof_image = prof_img)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/resetpass', methods=['post', 'get'])
def reset_link():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form1 = ReqresetForm()
    if form1.validate_on_submit():
        user = User.query.filter_by(email=form1.email.data).first()
        sendresetemail(user)
        flash('password reset link is sent to ur email', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_pass_link.html', title= '- RESET PASSWORD', form=form1)
    
@users.route('/passreset/<token>', methods=['post', 'get'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_token(token)
    if user is None:
        flash('Token Expired please send another one to reset ur password', 'warning')
        return redirect(url_for('users.reset_link'))
    form = ResetpassForm()
    if form.validate_on_submit():
        x = form.Password.data
        pass_hash = bcrypt.generate_password_hash(x).decode('utf-8')
        user.password = pass_hash
        db.session.commit()
        flash(f'password updated!', 'success')
        return redirect(url_for('users.login'))
    return render_template('resettoken.html', title= '- RESET PASSWORD', form=form)

@users.route('/pass-reset', methods=['get', 'post'])
def numpass():
    code = request.args.get('hasher')
    user = request.args.get('username')
    user = User.query.filter_by(username=user).first()
    form = ReqresetnumForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(code, str(form.num.data)):
            hashed = user.get_reset_token(300)
            return redirect(url_for('users.reset_token', token=hashed))
        else:
            flash('please enter correct code that is sent to ur mobile', 'danger')
    return render_template('resetnum.html', titles = ' - Reset Password', form=form)


@users.route('/numreset', methods=['get', 'post'])
def numreset():
    form = ReqnumForm()
    if form.validate_on_submit():
        num = form.number.data
        uname = form.username.data
        x = byNum(uname, num)
        code = bcrypt.generate_password_hash(str(x['code'])).decode('utf-8')
        return redirect(url_for('users.numpass', username = x['userid'], hasher=code))
    return render_template('pass-reset-num.html', titles=' - Reset Password', form=form)

















