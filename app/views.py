from datetime import datetime
from flask import abort, render_template, url_for, redirect, request, g, session
from flask_login import login_user, logout_user, current_user, \
    login_required
from werkzeug.security import generate_password_hash
from app import app, db, login_manager
from app.forms import AddUserForm, EditUserForm
from app.models import User
from config import TITLE, USERS_PER_PAGE

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(403)
def not_found_error(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/users')
def users():
    users = User.query.all()


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
@login_required
def index(page=1):
    users = User.query.paginate(page, USERS_PER_PAGE, False)
    return render_template('index.html', title = TITLE, users = users)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(username = username).first()
    if registered_user is None:
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        return redirect(url_for('login'))
    login_user(registered_user, remember = remember_me)
    return redirect(url_for('index'))


@app.route('/edit/<int:user_id>', methods = ['GET', 'POST'])
@login_required
def edit_user(user_id):
    if g.user.role != 0:
        return abort(403)
    if user_id != 1:
        user = User.query.filter_by(id=user_id).first()
        form = EditUserForm(user.username,user.name,user.password,user.role)
        if form.validate_on_submit():
            user.name = form.name.data
            user.username = form.username.data
            user.password = form.password.data
            user.role = form.role.data
            rows = User.query.filter_by(id=user_id).update({
                    'name': user.name,
                    'username': user.username,
                    'password': generate_password_hash(user.password),
                    'role': user.role
                    })
            db.session.commit()
            return redirect(url_for('index'))
        elif request.method != "POST":
            form.name.data = user.name
            form.username.data = user.username
            form.password.data = user.password
            form.role.data = user.role
        return render_template('edit_user.html', form=form)
    else:
        return abort(403)


@app.route('/delete/<int:user_id>', methods = ['GET', 'POST'])
@login_required
def delete_user(user_id):
    if g.user.role != 0:
        return abort(403)
    if user_id != 1:
        user = User.query.filter_by(id=user_id).first()
        form = EditUserForm(user.username,user.name,user.password,user.role)
        if form.validate_on_submit():
            rows = User.query.filter_by(id=user_id).delete()
            db.session.commit()
            return redirect(url_for('index'))
        elif request.method != "POST":
            form.name.data = user.name
            form.username.data = user.username
            form.password.data = user.password
            form.role.data = user.role
        return render_template('delete_user.html', form=form)
    else:
        return abort(403)


@app.route('/add', methods = ['GET', 'POST'])
@login_required
def add_user():
    if g.user.role != 0:
        return abort(403)
    form = AddUserForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,username=form.username.data,password=form.password.data,role=form.role.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_user.html', form = form)


@app.route('/add-with-request', methods = ['GET', 'POST'])
@login_required
def add_user_request():
    if g.user.role != 0:
        return abort(403)
    if request.method == 'POST':
        user = User(name=request.form['name'],username=request.form['username'],password=request.form['password'],role=request.form['role'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_user_request.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/test500page')
@login_required
def test_500_page():
    return abort(500)
