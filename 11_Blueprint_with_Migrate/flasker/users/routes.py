from flask import Blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user,login_required
from flasker import db, login_manager
from flasker.models import Users, Posts
from flasker.users.forms import UserForm, LoginForm

usersapp=Blueprint('usersapp',__name__)

@usersapp.route('/register',methods=['POST','GET'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        name=form.name.data.strip().lower().title()
        username=form.username.data
        password=form.password.data
        location=form.location.data.strip().lower().title()
        user=Users.query.filter_by(username=username).first()
        if not user:
            user=Users(name=name,username=username,location=location,password=password)
            try:
                db.session.add(user)
                db.session.commit()
                flash(f'User {name} with username {username} commited successfully to DataBase!','success')
            except:
                flash(f"Error while adding name:{name} -username:{username} to DataBase","danger")
            form.name.data=''
            form.username.data=''
            form.location.data=''
        else:
            flash(f'username:{user.username} allready Exist added by User {user.name} at {user.date}!!!','warning')
    users=Users.query.order_by(Users.date_added)
    return render_template('register.html',users=users,form=form)

@usersapp.route('/dashboard',methods=['POST','GET'])
@login_required
def dashboard():
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
    return render_template('Dashboard.html',form=form)

@usersapp.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password=form.password.data
        user=Users.query.filter_by(username=username).first()
        if user:
            if password==user.password:
                login_user(user)
                flash('User Logged in Successsfully','success')
                nextpage=request.args.get('next')
                return redirect(nextpage) if nextpage else redirect(url_for('usersapp.dashboard'))
            else:
                flash('wrong password try again','warning')
        else:
            flash('wrong username','warning')
    return render_template('login.html',form=form)

@usersapp.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    flash(f'logged out successfully','info')
    return redirect(url_for('mainapp.home'))
