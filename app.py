import datetime
from os import getenv

from flask import Flask, redirect, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

from forms import LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect('/login')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    from table import User
    form = LoginForm()
    if form.validate_on_submit():
        session = db.session
        user = list(filter(lambda x: x.hashed_password and x.check_password(form.password.data), list(session.query(User))))
        if len(user) > 1:
            return render_template('login.html',
                                   message="Удивительным образом у другого пользователя такой же хэш пароля.<br>"
                                           "Сделайте себе новый",
                                   form=form)
        if not user:
            return render_template('login.html',
                                   message="Нет пользователя с таким паролем",
                                   form=form)
        user = user[0]
        if user.password_time < datetime.datetime.now():
            return render_template('login.html',
                                   message="Срок действия пароля истёк",
                                   form=form)
        login_user(user, remember=form.remember_me.data)
        return redirect("/")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/login")


@login_required
@app.route('/users')
def users():
    from table import User
    if request.args.get('kick'):
        db.session.query(User).filter(User.id == request.args.get('kick')).delete()
        db.session.commit()
        return redirect('/users')
    u = current_user.group.users
    return render_template('users.html', users=u)


@login_required
@app.route('/teachers')
def teachers():
    from table import User
    t = current_user.group.teachers
    if current_user.access < 1:
        return render_template('teachers_user.html', teachers=t)
    else:
        return render_template('teachers_admin.html', teachers=t)


@login_required
@app.route('/update_db', methods=['POST'])
def update_db():
    return '^^'


@login_manager.user_loader
def load_user(user_id):
    session = db.session
    from table import User
    return session.query(User).get(user_id)


if __name__ == '__main__':
    app.run()
