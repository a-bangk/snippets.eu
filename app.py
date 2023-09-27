
from flask import Flask, render_template, request, flash, redirect, url_for
import re
import sourcemanagement as sm
from dbconnections import get_db_connection
import notemanagement as nm
import tagmanagement as tm
import sourcemanagement as sm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HGrsAtU^Bt7cV8D5'

#@app.route('/')
#def index():
#    snippets=nm.listNotes()
#    return render_template('index.html', items=snippets)


@app.route('/', methods=('GET', 'POST'))
def index():
    sourceString=""
    sourceUrl=""
    tagString=""
    contentString=""
    snippetId=False
    if request.method == 'POST':
        if request.form['action'] == 'Add':
            content = request.form['content']
            sourceString = request.form['sources-auto']
            snippetId=request.form['snippet-id']
            source_url=request.form['source-url']
            tagString=request.form['tags-auto'].strip()
            tagList=tagString.split(',')
            authorsString=request.form['authors-auto'].strip()
            authorList=authorsString.split(',')
            if not content:
                flash('Content is required!')
                return redirect(url_for('index'))
            if authorsString and not (sourceString or sourceUrl):
                flash('Author entry requires Source Title or URL')
                return redirect(url_for('index'))
            nm.alterSnippet(content,sourceString,tagList,source_url,authorList,snippetId)
        elif request.form['action'] == 'Delete':
            nm.deleteSnippet(request.form.getlist('delete-checks'))
        elif re.search("Edit*",request.form['action']):
            id=re.findall(r'\d+',request.form['action'])
            existingSnippet=nm.editSnippet(id)
            contentString=existingSnippet['content']
            sourceString=existingSnippet['sources']
            sourceUrl=existingSnippet['url']
            tagString=existingSnippet['tags']
            snippetId=existingSnippet['id']
    snippets=nm.listNotes()
    tags=tm.listTags()
    sources = sm.listSourceTitles()
    authors = sm.listAuthors()
    return render_template('index.html', items=snippets, tags=tags, sources=sources,authors=authors, previous_source=sourceString, previous_url=sourceUrl,previous_tags=tagString, previous_content=contentString, previous_id=snippetId)



@app.route('/filtersnippetslist/', methods=('GET', 'POST'))
def filtersnippetslist():
    tags=tm.listTags()
    if request.method == 'POST':
        tagValues = request.form.getlist('tag-checks')
        filter = request.form['filter_logic']
        snippets=nm.listTaggedNotes(tagValues,filter)
    else:
        snippets=nm.listNotes()
    return render_template('filtersnippetslist.html', items=snippets, tags=tags)


@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/source/', methods=('GET', 'POST'))
def source():
    sourcesList=sm.listSources()
    sourceTypesDict=sm.dictSourceTypes()
    if request.method == 'POST':
        if request.form['action'] == 'Add':
            if not request.form['title'] and request.form['source_type']:
                flash('A title and source type is required!')
                return redirect(url_for('source'))        
            sourceTypeId = [d.get('id') for d in sourceTypesDict if d.get('entry')==request.form['source_type']]
            sm.addSource(request.form['author_forename'],request.form['author_surname'],request.form['author_middlename'],request.form['author_postnominal'],request.form['author_title'],request.form['title'],request.form['year'],sourceTypeId[0],request.form['url'])
            sourcesList=sm.listSources()
        elif request.form['action'] == 'Delete':
            sm.deleteSource(request.form.getlist('delete-checks'))
    return render_template('source.html', sources=sourcesList, sourceTypes=sourceTypesDict)

@app.route('/author/', methods=('GET', 'POST'))
def author():
    authorList=listAuthors()
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    if request.method == 'POST':
        authorFullname = str(request.form['author_fullname'])
        comment = str(request.form['author_comment'])
        birthyear = str(request.form['author_birthyear'])
        print(birthyear)
        deathyear = str(request.form['author_deathyear'])
        if not authorFullname:
            flash('Name required!')
            return redirect(url_for('author'))
        cur.execute(f'insert into author(full_name,birthyear, deathyear, comment) VALUES ("{authorFullname}","{birthyear}","{deathyear}","{comment}");')
        conn.commit()
        conn.close()
        authorList=listAuthors()
    return render_template('author.html', authors=authorList)

def listAuthors():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('SELECT full_name as fullname, IFNULL(birthyear,"") as birthyear,IFNULL(deathyear,"") as deathyear, comment from author order by id desc;'.format(str()))
    db_authors=cur.fetchall()
    conn.close()
    authors=[]
    for author in db_authors:
        authors.append(author)
    return authors

@app.route('/tag/', methods=('GET', 'POST'))
def tag():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True) 
    if request.method == 'POST':
        if request.form['action']=='Add':
            tag = request.form['tag']
            if not tag:
                flash('Tag is required!')
                return redirect(url_for('tag'))
            cur.execute(f'insert into notetag(tag,entry_datetime, update_datetime) VALUES ("{tag}", now(), now())')
        if request.form['action']=='Delete':
            tm.deleteTags(request.form.getlist('delete-checks'))
        conn.commit()
        conn.close()
    tags=tm.listTagsFull()
    return render_template('tag.html', items=tags)

