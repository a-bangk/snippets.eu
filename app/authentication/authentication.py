from flask import render_template, flash, redirect, url_for,request, session
from app.forms import LoginForm
from flask_login import current_user, login_user,logout_user
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import time

from . import login_bp
from ..models import User

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            session['login_attempts'] = session.get('login_attempts', 0) + 1
            sleep_time = min(2 ** session['login_attempts'], 30)
            time.sleep(sleep_time) 
            flash('Invalid username or password')
            return redirect(url_for('login_bp.login'))
        session.pop('login_attempts', None)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home_bp.index')
        return redirect(url_for('home_bp.index'))
    return render_template('login.html', title='Sign In', form=form)

@login_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))