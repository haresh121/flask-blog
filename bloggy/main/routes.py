from flask import Blueprint
from time import sleep
from flask import render_template,redirect, url_for, request,flash
from bloggy import db
from flask import current_app as app
from bloggy.models import Posts,Comments,Todo
from flask_login import current_user,login_required
from sqlalchemy.sql.expression import desc

main = Blueprint('main', __name__)




@main.route('/')
@main.route('/home', methods=['post', 'get'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts=Posts.query.order_by('id desc').paginate(page=page, per_page=5)
    post_num = request.args.get('post_num')
    if post_num:
        post_num = int(post_num)
        if request.method == 'POST':
            com = request.form['comm']
            c = Comments( comment = com, post_id=post_num, user_id = current_user.id)
            db.session.add(c)
            db.session.commit()
            comms = Comments.query.all()
            posts_page = int(request.args.get('post_page'))
            return redirect(url_for('main.home', page=posts_page))
    comms = Comments.query.all()
    return render_template('home.html', posts=posts, titles= '', comments=comms)

@main.route('/about')
def about():
    return render_template('info.html', titles=' - Information')



@main.route('/todo', methods=['post', 'get'])
@login_required
def todo():
    if request.method == 'POST':
        
        t = request.form['todo']
        todo = Todo(todo=t, user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        todo = Todo.query.filter_by(user_id = current_user.id)
        return render_template('todo.html', titles=' - TODO', todos=todo)
    todo = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('todo.html', titles=' - TODO', todos=todo)

@main.route('/deltodo')
@login_required
def deltodo():
    x = int(request.args.get('t_n_d'))
    x = Todo.query.get_or_404(x)
    db.session.delete(x)
    db.session.commit()
    return redirect(url_for('main.todo'))











