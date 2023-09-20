
from flask import Flask, render_template, request, flash, redirect, url_for
import sourcemanagement as sm
from dbconnections import get_db_connection
import notemanagement as nm
import tagmanagement as tm
import sourcemanagement as sm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'HGrsAtU^Bt7cV8D5'

@app.route('/')
def index():
    notes=nm.listNotes()
    return render_template('index.html', notes=notes)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    sourceString=""
    sourceUrl=""
    tagString=""
    if request.method == 'POST':
        if request.form['action'] == 'Add':
            content = request.form['content']
            source = request.form['sources-auto']
            sourceString=source
            source_url=request.form['source-url']
            tagString=request.form['tags-auto'].strip()
            tagList=tagString.split(',')
            if not content:
                flash('Content is required!')
                return redirect(url_for('index'))
            nm.addNote(content,source,tagList,source_url)
        elif request.form['action'] == 'Delete':
            nm.deleteSnippet(request.form.getlist('delete-checks'))
        elif request.form['action'] == 'Edit':
            nm.editSnippet(request.form.getlist('edit-snippet'))
    snippets=nm.listNotes()
    tags=tm.listTags()
    sources = sm.listSourceTitles()
    print(sourceString)
    return render_template('create.html', items=snippets, tags=tags, sources=sources, previous_source=sourceString, previous_url=sourceUrl,previous_tags=tagString)



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
        forename = str(request.form['author_forename'])

        author_title = str(request.form['author_title'])
        surname = str(request.form['author_surname'])
        middlename = str(request.form['author_middlename'])
        postnominal = str(request.form['author_postnominal'])
        birthyear = str(request.form['author_birthyear'])
        deathyear = str(request.form['author_deathyear'])
        if not forename and not surname and not middlename and not postnominal and not birthyear and not deathyear:
            flash('One field is required!')
            return redirect(url_for('author'))
        cur.execute(f'insert into author(forename,surname,title,postnominal,middlename,birthyear, deathyear) VALUES ("{forename}","{surname}","{author_title}","{postnominal}","{middlename}","{birthyear}","{deathyear}")')
        conn.commit()
        conn.close()
        authorList=listAuthors()
    return render_template('author.html', authors=authorList)

def listAuthors():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('SELECT IFNULL(title,"") as title, IFNULL(forename,"") as forename,IFNULL(surname,"") as surname,IFNULL(middlename,"") as middlename,IFNULL(postnominal,"") as postnominal,IFNULL(birthyear,"") as birthyear,IFNULL(deathyear,"") as deathyear from author order by id desc;'.format(str()))
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

