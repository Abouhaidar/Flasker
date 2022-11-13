from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import current_user, login_user, logout_user,login_required
from flasker import db, login_manager
from flasker.models import Users, Posts, DeletedPosts
from flasker.users.forms import UserForm, LoginForm
from datetime import datetime

adminapp=Blueprint('adminapp',__name__)


@adminapp.route('/delpost/<int:id>')
def delpost(id):
    post=DeletedPosts.query.get_or_404(id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted Endgültig','success')
    else:
        flash('post cant be deleted try again','danger')
    return redirect(url_for('adminapp.admindashboard'))

@adminapp.route('/admindashboard',methods=['POST','GET'])
@login_required
def admindashboard():
    admin=Users.query.filter_by(username='lilian').first()
    if admin:
        admin.isadmin=True
        db.session.commit()
        if current_user.isadmin:
            form = UserForm()
            id=current_user.id
            user=Users.query.get_or_404(id)

            if request.method=='POST':
                name=form.name.data.strip().lower().title()
                username=form.username.data
                location=form.location.data.strip().lower().title()
                user.name=name
                user.username=username
                user.location=location
                try:
                    db.session.commit()
                    flash(f'User {name} with username {username} updated successfully and commited to DataBase!','success')
                except:
                    flash(f"Error while updating name:{name} -username:{username} to DataBase","danger")
            else:
                form.name.data=user.name
                form.username.data=user.username
                form.location.data=user.location
            users=Users.query
            return render_template('admindashboard.html',form=form,users=users)
        else:
            return redirect(url_for('usersapp.dashboard'))
    else:
        return redirect(url_for('usersapp.login'))

@adminapp.route('/recoverpost/<int:id>',methods=['POST','GET'])
@login_required
def recoverpost(id):
    if current_user.isadmin:
        post_to_recover=DeletedPosts.query.get_or_404(id)
        if post_to_recover:
            post=Posts(title=post_to_recover.title,
                       subject=post_to_recover.subject,
                       content=post_to_recover.content,
                       user_id=post_to_recover.user_id)
            try:
                db.session.add(post)
                db.session.delete(post_to_recover)
                db.session.commit()
                flash(f'Post: recovered Successfully to UserID','success')
            except:
                flash('Error while Commiting to DataBase Try again!!','danger')
        else:
            flash('Error Post not found','info')
        return redirect(url_for('adminapp.admindashboard'))
    else:
        flash('You are not admin to do that!!!','info')
        return redirect(url_for('usersapp.dashboard'))