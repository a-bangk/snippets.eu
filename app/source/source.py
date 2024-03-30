
from flask import Flask, render_template, request, flash, redirect, url_for
import re
import json
from flask_login import login_required, current_user

from ..helperfunctions import get_db_connection
from .. import authormanagement as am
from .. import notemanagement as nm
from .. import tagmanagement as tm
from . import management as sm
from . import source_bp


@source_bp.route('/source', methods=('GET', 'POST'))
@login_required
def source():
    exisitingTitle=''
    exisitingYear=''      
    exisitingUrl=''
    exisitingFullname=''
    exisitingType=''
    sourceTypesDict=sm.dictSourceTypes()
    id=''
    if request.method == 'POST':
        if request.form['action'] == 'Add':
            if request.form['source_type'] == "None" or request.form['source_type']=='':
                flash('Sources require a type selected')
                return redirect(url_for('source_bp.source'))
            else:
                sourceTypeId = [d.get('id') for d in sourceTypesDict if d.get('entry')==request.form['source_type']][0]
            if not request.form['title'] or sourceTypeId == None:
                flash('A title and source type is required!')
                return redirect(url_for('source_bp.source'))
            authorString=request.form['authors-auto'].strip()
            authorList=authorString.split(',')
            while("" in authorList):
                authorList.remove("")
            sm.alterSource(authorList,request.form['title'],request.form['year'],sourceTypeId,request.form['url'],request.form['source_id'],current_user.id)
        elif re.search("Edit*",request.form['action']):
            id=re.findall(r'\d+',request.form['action'])[0]
            existingSource=sm.loadSource(id)
            exisitingTitle=existingSource['title']
            exisitingYear=existingSource['year']
            exisitingUrl=existingSource['url']
            exisitingFullname=existingSource['author']
            exisitingType=existingSource['type']
        elif request.form['action'] == 'Delete':
            sm.deleteSource(request.form.getlist('delete-checks'))
    sourcesList=sm.listSourcesForUserId(current_user.id)
    authors = am.listAuthorsAutoForUserId(current_user.id)
    return render_template('source.html', sources=sourcesList, sourceTypes=sourceTypesDict, title=exisitingTitle, year=exisitingYear, url=exisitingUrl, type=exisitingType, previous_authors=exisitingFullname, previous_id=id, authors=authors )

@source_bp.route('/<user_username>/source=<source_id>', methods=('GET', 'POST'))
@login_required
def source_sorted(user_username,source_id):
    tags2=tm.tagsForUserIdSortable(current_user.id)
    tags=tm.tagsForUserIdWithCount(current_user.id)
    source_fields=sm.loadSource(source_id)
    snippets=nm.listNotesForUserIdSourceId(current_user.id, source_id)
    for dictionary in snippets:
        dictionary['exploreSource']=f'/{user_username}/source={source_id}'
    snippets=json.dumps(snippets)
    return render_template('exploreSource.html', items=snippets, tags=tags, tags2=tags2, source=source_fields)