# -*- coding: utf-8 -*-

"""
app.blueprints.pages.routes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The profile routes for spa-base.
"""

from flask import (
	Blueprint,
	flash,
	redirect,
	render_template,
	request,
	url_for,
)
from flask_login import current_user, login_required

from app.models import db, User
from .forms import EditProfileForm


blueprint = Blueprint('profile', __name__, template_folder='templates')


@blueprint.route('/user/<email>')
@login_required
def profile(email):
	user = User.query.filter_by(email=email).first_or_404()
	return render_template('profile/profile.html', user=user)


@blueprint.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.email)
	if form.validate_on_submit():
		current_user.email = form.email.data
		current_user.first_name = form.first_name.data
		current_user.last_name = form.last_name.data
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('profile.profile', email=current_user.email))
	elif request.method == 'GET':
		form.email.data = current_user.email
		form.first_name.data = current_user.first_name
		form.last_name.data = current_user.last_name
	return render_template('profile/profile_form.html', title='Edit Profile',
						   form=form)


#from datetime import datetime

#@app.before_request
#def before_request():
#	if current_user.is_authenticated:
#		current_user.last_seen = datetime.utcnow()
#		db.session.commit()
