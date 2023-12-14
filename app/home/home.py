
from flask import render_template, request, flash, redirect, url_for
from .. import helperfunctions as hf
from .. import tagmanagement as tm
from .. import notemanagement as nm
from .. import authormanagement as am
from .. source import management as sm
from . import home_bp
import re


@home_bp.route('/', methods=('GET', 'POST'))
def index(authorsString="",sourceString="",sourceUrl="",tagString="", contentString="", snippetsId=""):
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
            snippetId=request.form['snippet-id']
            sourceUrl=request.form['source-url']
            tagString=request.form['tags-auto']
            tagList=hf.commaStringToList(tagString)
            authorsString=request.form['authors-auto']
            authorList=hf.commaStringToList(authorsString)
            authorList=authorsString.split(',')
            if not content:
                flash('Content is required!')
                return redirect(url_for('home_bp.index'))
            if authorsString and not (sourceString or sourceUrl):
                flash('Author entry requires Source Title or URL')
                return redirect(url_for('home_bp.index'))
            nm.alterSnippet(content,sourceString,tagList,sourceUrl,authorList,snippetId)
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
    snippets=nm.listNotes()
    tags=tm.listTags()
    sources = sm.listSourceTitles()
    authors = am.listAuthorsAuto()
    return render_template('index.html', items=snippets, tags=tags, authors=authors,sources=sources,previous_authors=authorsString, previous_source=sourceString, previous_url=sourceUrl,previous_tags=tagString, previous_content=contentString, previous_id=snippetId)


