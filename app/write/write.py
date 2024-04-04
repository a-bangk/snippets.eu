from flask import render_template, request, flash, redirect, url_for, Blueprint
import json
from .. import helperfunctions as hf
from .. import tagmanagement as tm
from .. import notemanagement as nm
from .. import authormanagement as am
from .. source import management as sm
from . import write_bp
import re
from flask_login import current_user, login_required


filter_bp = Blueprint('filter_bp', __name__)

@write_bp.route('/write', methods=('GET', 'POST'))
@login_required
def write():
    sourceString=""
    sourceUrl=""
    tagString=""
    contentString=""
    authorsString=""
    snippetId=False
    if request.method == 'POST':
        if request.form['action'] == 'Add':
            content = request.form['content']
            sourceString = request.form['sources-auto']
            if sourceString=="":
                authorsString=hf.username_from_user_id(current_user.id)
                sourceString=authorsString + "'s Notes"
            snippetId=request.form['snippet-id']
            sourceUrl=request.form['source-url']
            tagString=request.form['tags-auto']
            if tagString =="":
                tagString="unsorted"
            tag_list=hf.commaStringToList(tagString)
            authorsString=request.form['authors-auto']
            if authorsString=="":
                authorsString=hf.username_from_user_id(current_user.id)
            authorList=hf.commaStringToList(authorsString)
            authorList=authorsString.split(',')
            if not content:
                flash('Content is required!')
                return redirect(url_for('write_bp.write'))
            if (authorsString !="" and sourceUrl !="") and sourceString=="":
                flash('Author or URL entries require a Source Title')
                return redirect(url_for('write_bp.write'))
            nm.alter_snippet(content,sourceString,tag_list,sourceUrl,authorList,snippetId,current_user.id)
            snippetId=False
        elif request.form['action'] == 'Delete':
            nm.deleteSnippet(request.form.getlist('delete-checks'))
        elif re.search("Edit*",request.form['action']):
            id=re.findall(r'\d+',request.form['action'])
            existingSnippet=nm.editSnippet(id[0])
            contentString=existingSnippet['content']
            sourceString=existingSnippet['sources']
            if sourceString is None:
                sourceString=''
            sourceUrl=existingSnippet['url']
            if sourceUrl is None:
                sourceUrl=''
            tagString=existingSnippet['tags']
            snippetId=existingSnippet['id']
            authorsString=am.authorsStringFromNoteId(snippetId)
    snippets=nm.list_notes_user_id_recent_14(current_user.id)
    snippets=json.dumps(snippets)

    tags=tm.tagsForUserId(current_user.id)
    sources = sm.sourceTitlesForUserId(current_user.id)
    authors = am.listAuthorsAutoForUserId(current_user.id)
    return render_template('write.html', 
                           items=snippets, tags=tags, authors=authors,
                           sources=sources,previous_authors=authorsString, 
                           previous_source=sourceString, 
                           previous_url=sourceUrl,
                           previous_tags=tagString, 
                           previous_content=contentString, 
                           previous_id=snippetId)

@write_bp.route('/update-tags')
def redirect_to_update_tags():
    # Redirecting to a route in the first blueprint
    return redirect(url_for('filter_bp.update_tags'))


@write_bp.route('/update-content', methods=['POST'])
@login_required
def redirect_to_update_snippet():
    return redirect(url_for('filter_bp.update_snippet'))

# Adjusted route definition
@write_bp.route('/get-updated-content', methods=['GET'])
@login_required
def redirect_to_get_updated_content():
    return redirect(url_for('filter_bp.get_updated_content'))