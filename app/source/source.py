
from flask import Flask, render_template, request, flash, redirect, url_for
import re

from ..helperfunctions import get_db_connection
from .. import helperfunctions as hf
from .. import notemanagement as nm
from .. import tagmanagement as tm
from .. import authormanagement as am

from dynaconf import FlaskDynaconf
from . import source_bp



@source_bp.route('/source/', methods=('GET', 'POST'))
def source():
    exisitingTitle=''
    exisitingYear=''      
    exisitingUrl=''
    exisitingFullname=''
    exisitingType=''
    sourceTypesDict=dictSourceTypes()
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
            alterSource(authorList,request.form['title'],request.form['year'],sourceTypeId,request.form['url'],request.form['source_id'])
        elif re.search("Edit*",request.form['action']):
            id=re.findall(r'\d+',request.form['action'])[0]
            existingSource=loadSource(id)
            exisitingTitle=existingSource['title']
            exisitingYear=existingSource['year']
            exisitingUrl=existingSource['url']
            exisitingFullname=existingSource['author']
            exisitingType=existingSource['type']
        elif request.form['action'] == 'Delete':
            deleteSource(request.form.getlist('delete-checks'))
    sourcesList=listSources()
    authors = am.listAuthorsAuto()
    return render_template('source.html', sources=sourcesList, sourceTypes=sourceTypesDict, title=exisitingTitle, year=exisitingYear, url=exisitingUrl, type=exisitingType, previous_authors=exisitingFullname, previous_id=id, authors=authors )

def listSources():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('select st.entry as type,s.id,s.title as title, GROUP_CONCAT(a.full_name SEPARATOR ", ") as author,a.id as a_id, s.url as url from source s left join associate_source_author aa on s.id = aa.source_id left join author a on aa.author_id = a.id left join source_type st on s.source_type_id = st.id group by s.id order by s.id desc;')
    db_sources=cur.fetchall()
    conn.close()
    sources=[]
    for source in db_sources:
        sources.append(source)
    return sources

def listSourceTitles():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('select s.title as title, s.id as id from source s;')
    db_sources=cur.fetchall()
    conn.close()
    sources=[]
    for source in db_sources:
        if source:
            sources.append(source['title'])
    return sources

def dictSourceTypes():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('select id,entry from source_type st;')
    dictSourceTypes=cur.fetchall()
    conn.close()
    return dictSourceTypes

def alterSource(authorFullNameList, title, year, typeId, url,sId):
    if year=='':
        year is None
    if url=='':
        url is None
    if sId == '':
        sId=addSource(title,typeId,url,year)
    else:
        updateSource(title,url,typeId,year,sId)
    authorIds=am.idFromFullNamesList(authorFullNameList)
    asm.linkAuthorsToSource(sId,authorIds)

def deleteSource(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    for id in delete_ids:
        sql='delete from source where id=?;'
        cur.execute(sql,(id,))
        sql='delete ignore from associate_source_note where source_id=?;'
        cur.execute(sql,(id,))
        sql='delete ignore from associate_source_author where source_id=?;'
        cur.execute(sql,(id,))
    conn.commit()
    conn.close()

def loadSource(edit_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql='select st.entry as type,s.id,s.year as year, s.title as title, GROUP_CONCAT(a.full_name SEPARATOR ", ") as author, s.url as url from source s left join associate_source_author aa on s.id = aa.source_id left join author a on aa.author_id = a.id left join source_type st on s.source_type_id = st.id where s.id=?;'
    cur.execute(sql,(edit_id,))
    previousSnippet=cur.fetchone()
    conn.close()
    return(previousSnippet)

def addSource(title, typeId, url, year):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql='insert into source(title,entry_datetime, update_datetime,source_type_id,url,year) VALUES (?, now(),now(),?, ?, ?);'
    cur.execute(sql,(title,typeId,url,year))
    sId = cur.lastrowid
    conn.commit()
    conn.close()
    return(sId)

def linkAuthor(sourceId, authorId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql='INSERT INTO associate_source_author (author_id, source_id) VALUES (?, ?);'
    cur.execute(sql,(authorId,sourceId))
    conn.close()

def updateSource(title,url,typeId,year,sourceId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql='update source set title = ?,update_datetime=now(),url=?, source_type_id=?, year=? where id = ?;'
    cur.execute(sql,(title,url,typeId,year,sourceId))
    conn.commit()
    conn.close()

def idFromTitle(title):
    conn = get_db_connection()
    cur=conn.cursor()
    sql='SELECT id from source where title = ?;'
    cur.execute(sql,(title,))
    id=cur.fetchone()
    if not id:
        sql='INSERT INTO source (title,entry_datetime,update_datetime) values (?, now(),now());'
        cur.execute(sql,(title,))
        id=cur.lastrowid
        conn.commit()
    else:
        id=id[0]     
    conn.close()
    return id

def idFromUrl(url):
    conn = get_db_connection()
    cur=conn.cursor()
    sql='SELECT id from source where url = ?;'
    cur.execute(sql,(url,))
    id=cur.fetchone()
    if not id:
        sql='INSERT INTO source (url,entry_datetime,update_datetime) values (?, now(),now());'
        cur.execute(sql,(url,))
        id=cur.lastrowid
        conn.commit()
    else:
        id=id[0]     
    conn.close()
    return id

def idFromTitleAndUrl(title,url):
    conn = get_db_connection()
    cur=conn.cursor()
    sql='SELECT id from source where title = ? and url=?;'
    cur.execute(sql,(title,url))
    id=cur.fetchone()
    if not id:
        sql='INSERT INTO source (title,entry_datetime,update_datetime,url) values (?, now(),now(),?);'
        cur.execute(sql,(title,url))
        id=cur.lastrowid
        conn.commit()
    else:
        id=id[0]     
    conn.close()
    return id