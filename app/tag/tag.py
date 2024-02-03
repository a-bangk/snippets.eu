from flask import render_template, request, flash, redirect, url_for
from .. import helperfunctions as hf
from .. import tagmanagement as tm
from . import tag_bp

from flask_login import login_required,current_user

@tag_bp.route('/tag', methods=('GET', 'POST'))
@login_required
def tag():
    if request.method == 'POST':
        if request.form['action']=='Add':
            tag = request.form['tag']
            if not tag:
                flash('Tag is required!')
                return redirect(url_for('tag_bp.tag'))
            tm.addTagForUser(tag,current_user.id)
        if request.form['action']=='Delete':
            tm.deleteTagsById(request.form.getlist('delete-checks'))
    tags=tm.tagsAllFieldsForUserId(current_user.id)
    return render_template('tag.html', items=tags)
