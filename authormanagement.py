from dbconnections import get_db_connection

def listAuthors():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('SELECT id,full_name as fullname, IFNULL(birthyear,"") as birthyear,IFNULL(deathyear,"") as deathyear, comment from author order by id desc;'.format(str()))
    db_authors=cur.fetchall()
    conn.close()
    authors=[]
    for author in db_authors:
        authors.append(author)
    return authors

def listAuthorsAuto():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=False)
    cur.execute('select full_name as author from author;')
    authors_db=cur.fetchall()
    conn.close()
    authors=[]
    for author in authors_db:
        authors.append(author[0])
    return authors

def editAuthor(edit_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute(f'SELECT id,full_name as fullname, IFNULL(birthyear,"") as birthyear,IFNULL(deathyear,"") as deathyear, comment from author a where a.id={edit_id};')
    author=cur.fetchone()
    conn.close()
    return(author)

def saveAuthor(fullName,birthyear,deathyear,comment, id=0):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    if id == 0:
        cur.execute(f'insert into author(full_name,birthyear,deathyear,comment) VALUES ("{fullName}", "{birthyear}", "{deathyear}", "{comment}");')
    else:
        cur.execute(f'update author set full_name = "{fullName}",birthyear = "{birthyear}",deathyear = "{deathyear}",comment = "{comment}" where id = "{id}";')
    conn.commit()
    conn.close()