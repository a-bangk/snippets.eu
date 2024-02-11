from flask import render_template
from . import error_bp

from flask_login import login_required,current_user

# Continue in errors.py

@error_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

