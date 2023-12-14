from flask import render_template
from . import about_bp


@about_bp.route('/about/')
def about():
    return render_template('about.html')