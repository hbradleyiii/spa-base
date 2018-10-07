# -*- coding: utf-8 -*-

"""
app.blueprints.auth.routes
~~~~~~~~~~~~~~~~~~~~~~~~~~

The auth routes for spa-base
"""

from flask import (
    abort,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app.models import User
from .forms import LoginForm


blueprint = Blueprint('auth', __name__, template_folder='templates')


@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email address or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login_form.html', title='Login', form=form)


@blueprint.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        abort(405)
    logout_user()
    return redirect(url_for('auth.login'))
