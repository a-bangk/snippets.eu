
from flask import render_template, request, flash, redirect, url_for
from .. import helperfunctions as hf
from .. import tagmanagement as tm
from .. import notemanagement as nm
from .. import authormanagement as am
from .. source import management as sm
from . import home_bp
import re
from flask_login import current_user, login_user,logout_user, login_required


@home_bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    return render_template('index.html')


