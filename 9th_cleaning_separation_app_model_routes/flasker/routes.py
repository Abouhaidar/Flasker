from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, LoginManager
from flasker import app,db
from flasker.models import Users, Posts
from flasker.forms import UserForm, PostForm, LoginForm



# Setting Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category='info'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
##############################

@app.route('/register',methods=['POST','GET'])
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

@app.route('/addpost',methods=['POST','GET'])
@login_required
def addpost():
    postform=PostForm()
    if postform.validate_on_submit():
        title=postform.title.data
        content=postform.content.data
        try:
            post=Posts(title=title,content=content,user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post added Successfully!!!','success')
        except:
            flash(f"Error while adding current Post to DataBase", "danger")
        postform.title.data=''
        postform.content.data=''
    posts=Posts.query
    return render_template('addpost.html',postform=postform,posts=posts)

@app.route('/')
@app.route('/home')
def home():
    users=Users.query.order_by(Users.date_added)
    posts=Posts.query
    return render_template('home.html',users=users,posts=posts)

@app.route('/dashboard',methods=['POST','GET'])
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

@app.route('/login',methods=['POST','GET'])
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
                return redirect(nextpage) if nextpage else redirect(url_for('dashboard'))
            else:
                flash('wrong password try again','warning')
        else:
            flash('wrong username','warning')
    return render_template('login.html',form=form)

@app.route('/logout',methods=['POST','GET'])
@login_required
def logout():
    logout_user()
    flash(f'logged out successfully','info')
    return redirect(url_for('home'))

@app.route('/editpost/<int:id>',methods=['POST','GET'])
@login_required
def editpost(id):
    form=PostForm()
    post=Posts.query.get_or_404(id)
    if post and form.validate_on_submit() and current_user.id==post.user_id:
        post.title=form.title.data
        post.content=form.content.data
        try:
            db.session.commit()
            flash('Post updated Successfully!!','success')
        except:
            flash('Error while Commiting to DataBase!!!!','warning')
        return redirect(url_for('dashboard'))
    elif post and current_user.id==post.user_id:
        form.title.data=post.title
        form.content.data=post.content
        return render_template('editpost.html',postform=form)
    else:
        flash('you cant update this post or post not found','danger')
        return redirect(url_for('dashboard'))
