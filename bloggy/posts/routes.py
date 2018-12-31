from flask import Blueprint
from flask import render_template,redirect, url_for, flash, request, abort
from bloggy import db
from flask import current_app as app
from bloggy.posts.forms import PostForm
from bloggy.models import User,Posts,Comments
from flask_login import current_user,login_required


posts = Blueprint('posts', __name__)



@posts.route('/post/new', methods=['post', 'get'])
@login_required
def newpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'post created {form.title.data} ', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', titles = '- New Post', form=form)

@posts.route('/post/<int:post_id>')
def viewpost(post_id):
    post = Posts.query.get_or_404(post_id)
    return render_template('viewpost.html', title=post.title, post=post)

@posts.route('/<post_name>')
def viewuser(post_name):
    post = User.query.filter_by(username = post_name).first_or_404()
    if post is not None:
        pic = url_for('static', filename='user-pics/'+post.image_file)
        return render_template('viewuser.html', title=post.username, post=post, pic=pic)
    else:
        return redirect(url_for('main.home'))



@posts.route('/post/<int:post_id>/update', methods=['post', 'get'])
@login_required
def update(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('updated successfully', 'success')
        return redirect(url_for('posts.viewpost', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('updatepost.html', titles = '- Update Post', form=form)



@posts.route('/post/<int:post_id>/delete', methods=['post'])
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('POST DELETED', 'danger')
    return redirect(url_for('main.home'))


@posts.route('/delcomment')
def delcomment():
    comment_num = request.args.get('com_num')
    posts_page = request.args.get('post_page')
    if comment_num and posts_page:
        comment_num = int(comment_num)
        posts_page = int(posts_page)
        comment = Comments.query.get_or_404(comment_num)
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('main.home',page=posts_page))
    

@posts.route('/search', methods=['get', 'post'])
def searcher():
    if request.method == 'POST':
        search_post = request.form['search']
        post = Posts.query.filter_by(title = search_post).first()
        if post:
            return render_template('searcher.html', post=post)
        else:
            flash('the post you are searching for is not present, please check the title', 'info')
    return render_template('searcher.html', post=None)






















