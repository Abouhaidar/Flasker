from flask import Blueprint, abort
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from flasker import db
from flasker.models import Users, Posts, DeletedPosts
from flasker.posts.forms import PostForm

postsapp=Blueprint('postsapp',__name__)

@postsapp.route('/addpost',methods=['POST','GET'])
@login_required
def addpost():
    postform=PostForm()
    if postform.validate_on_submit():
        title=postform.title.data
        content=postform.content.data
        subject=postform.subject.data
        try:
            post=Posts(title=title,content=content,user_id=current_user.id,subject=subject)
            db.session.add(post)
            db.session.commit()
            flash('Post added Successfully!!!','success')
            return redirect(url_for('adminapp.admindashboard')) if current_user.isadmin else redirect(url_for('usersapp.dashboard'))
        except:
            flash(f"Error while adding current Post to DataBase", "danger")
        postform.title.data=''
        postform.content.data=''
        postform.subject.data=''
    posts=Posts.query
    return render_template('addpost.html',postform=postform,posts=posts)

@postsapp.route('/editpost/<int:id>',methods=['POST','GET'])
@login_required
def editpost(id):
    form=PostForm()
    post=Posts.query.get_or_404(id)
    if post and form.validate_on_submit() and current_user.id==post.user_id:
        post.title=form.title.data
        post.content=form.content.data
        post.subject=form.subject.data
        try:
            db.session.commit()
            flash('Post updated Successfully!!','success')
        except:
            flash('Error while Commiting to DataBase!!!!','warning')
        return redirect(url_for('adminapp.admindashboard')) if current_user.isadmin else redirect(url_for('usersapp.dashboard'))
    elif post and current_user.id==post.user_id:
        form.title.data=post.title
        form.content.data=post.content
        form.subject.data=post.subject
        return render_template('editpost.html',postform=form)
    else:
        flash('you cant update this post or post not found','danger')
        return redirect(url_for('adminapp.admindashboard')) if current_user.isadmin else redirect(url_for('usersapp.dashboard'))

@postsapp.route('/delete_post/<int:id>',methods=['POST'])
@login_required
def delete_post(id):
    post=Posts.query.get_or_404(id)
    if post.creater==current_user:
        try:
            deletedpost=DeletedPosts(title=post.title,subject=post.subject,content=post.content,user_id=post.user_id)
            db.session.add(deletedpost)
            db.session.delete(post)
            db.session.commit()
            flash('Post Deleted Successfully!','success')
        except:
            flash('Error while Deleting commited to DataBase!','warning')
    else:
        flash('YOu are not allowed too delete this Post','danger')
        abort(403)
    return redirect(url_for('adminapp.admindashboard')) if current_user.isadmin else redirect(url_for('usersapp.dashboard'))


