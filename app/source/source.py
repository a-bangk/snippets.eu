
from flask import Flask, render_template, request, flash, redirect, url_for
import re

from ..helperfunctions import get_db_connection
from .. import authormanagement as am
from . import management as sm

from . import source_bp

@source_bp.route('/source', methods=('GET', 'POST'))
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
                return redirect(url_for('source'))
            else:
                sourceTypeId = [d.get('id') for d in sourceTypesDict if d.get('entry')==request.form['source_type']][0]
            if not request.form['title'] or sourceTypeId == None:
                flash('A title and source type is required!')
                return redirect(url_for('source'))
            authorString=request.form['authors-auto'].strip()
            authorList=authorString.split(',')
            while("" in authorList):
                authorList.remove("")
            sm.alterSource(authorList,request.form['title'],request.form['year'],sourceTypeId,request.form['url'],request.form['source_id'])
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
    sourcesList=sm.listSources()
    authors = am.listAuthorsAuto()
    return render_template('source.html', sources=sourcesList, sourceTypes=sourceTypesDict, title=exisitingTitle, year=exisitingYear, url=exisitingUrl, type=exisitingType, previous_authors=exisitingFullname, previous_id=id, authors=authors )
