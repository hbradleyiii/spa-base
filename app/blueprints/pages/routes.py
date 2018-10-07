# -*- coding: utf-8 -*-

"""
app.blueprints.pages.routes
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pages routes for spa-base.
"""

from flask import Blueprint, render_template


blueprint = Blueprint('pages', __name__, template_folder='templates')


@blueprint.route('/terms-and-conditions/')
def terms_and_conditions():
    return render_template('pages/terms-and-conditions.html',
                           title='Terms and Conditions')


@blueprint.route('/privacy-policy/')
def privacy_policy():
    return render_template('pages/privacy-policy.html', title='Privacy Policy')
