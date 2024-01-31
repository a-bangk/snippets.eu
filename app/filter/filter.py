from flask import render_template,request,redirect,url_for,flash   
from . import filter_bp
from .. import tagmanagement as tm
from .. import notemanagement as nm

from flask_login import login_required


@filter_bp.route('/filtersnippetslist', methods=('GET', 'POST'))
@login_required
def filtersnippetslist():

    tags=tm.listTags()
    if request.method == 'POST':
        if request.form['action'] =='filter':
            tagValues = request.form.getlist('tag-checks')
            filter = request.form['filter_logic']
            snippets=nm.listTaggedNotes(tagValues,filter)
        if request.form['action'] == 'Add':
            content = request.form['content']
            sourceString = request.form['sources-auto']
            snippetId=request.form['snippet-id']
            source_url=request.form['source-url']
            tagString=request.form['tags-auto'].strip()
            tagList=tagString.split(',')
            tagList = [item.strip() for item in tagList]
            authorsString=request.form['authors-auto'].strip()
            authorList=authorsString.split(',')
            authorList = [item.strip() for item in authorList]
            if not content:
                flash('Content is required!')
                return redirect(url_for('home_bp.index'))
            #sourceUrl was in the or on the next line.
            if authorsString and not (sourceString):
                flash('Author entry requires Source Title or URL')
                return redirect(url_for('home_bp.index'))
            nm.alterSnippet(content,sourceString,tagList,source_url,authorList,snippetId)
    else:
        snippets=nm.listNotes()
    return render_template('filtersnippetslist.html', items=snippets, tags=tags)