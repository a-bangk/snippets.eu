from flask import render_template,request,redirect,url_for,flash   
from . import filter_bp
from .. import tagmanagement as tm
from .. import notemanagement as nm

from flask_login import login_required, current_user


@filter_bp.route('/filtersnippetslist', methods=('GET', 'POST'))
@login_required
def filtersnippetslist():
    tags=tm.listTagsForUserId(current_user.id)
    if request.method == 'POST':
        if request.form['action'] =='filter':
            tagValues = request.form.getlist('tag-checks')
            filter = request.form['filter_logic']
            snippets=nm.listTaggedNotesForUserId(tagValues,filter,current_user.id)
        if request.form['action'] == 'Add':
            content = request.form['content']
            source_string = request.form['sources-auto']
            snippet_id=request.form['snippet-id']
            source_url=request.form['source-url']
            tagString=request.form['tags-auto'].strip()
            tag_list=tagString.split(',')
            tag_list = [item.strip() for item in tag_list]
            authorsString=request.form['authors-auto'].strip()
            author_list=authorsString.split(',')
            author_list = [item.strip() for item in author_list]
            if not content:
                flash('Content is required!')
                return redirect(url_for('home_bp.index'))
            if authorsString and not source_string:
                flash('Author entry requires Source Title or URL')
                return redirect(url_for('home_bp.index'))
            nm.alterSnippet(content,source_string,tag_list,source_url,author_list,snippet_id,current_user.id)
    else:
        snippets=nm.listNotesForUserId(current_user.id)
    return render_template('filtersnippetslist.html', items=snippets, tags=tags)