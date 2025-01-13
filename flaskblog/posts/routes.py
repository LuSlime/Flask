from flask import (render_template, url_for, flash,redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment, Like
from flaskblog.posts.forms import PostForm
from flaskblog.posts.utils import save_picture
posts = Blueprint('posts', __name__)




@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            form.validate_form()  # Call the custom validation explicitly
        except ValidationError as e:
            flash(str(e), 'danger')
            return render_template('create_post.html', title='New Post', form=form, legend='New Post')

        # Save picture if provided
        if form.picture.data:
            picture_file = save_picture(form.picture.data, folder='post_pics')
        else:
            picture_file = None

        # Create the post
        post = Post(
            title=form.title.data if form.title.data else '',  # Allow null title
            image_file=picture_file,  # Allow null image_file
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.desc()).all()
    is_liked = Like.query.filter_by(post_id=post_id, user_id=current_user.id).first()

    if request.method == 'POST':
        if 'comment' in request.form:
            content = request.form.get('content')
            if content:
                comment = Comment(content=content, user_id=current_user.id, post_id=post.id)
                db.session.add(comment)
                db.session.commit()
        elif 'like' in request.form:
            if is_liked:
                db.session.delete(is_liked)
            else:
                like = Like(user_id=current_user.id, post_id=post.id)
                db.session.add(like)
            db.session.commit()
        return redirect(url_for('posts.post', post_id=post.id))

    return render_template('post.html', post=post, comments=comments, is_liked=bool(is_liked))


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.image_file = form.picture.data
        if form.picture.data:
            post.image_file = save_picture(form.picture.data)
        db.session.commit()
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.picture.data = post.image_file
    return render_template('create_post.html', title='Update Post',form=form, legend='Update Post')



@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.home'))
