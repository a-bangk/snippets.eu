from .helperfunctions import get_db_connection
from . import associationmanagement as asm

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

def loadAuthor(edit_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql='SELECT id,full_name as fullname, IFNULL(birthyear,"") as birthyear,IFNULL(deathyear,"") as deathyear, comment from author a where a.id=?;'
    cur.execute(sql,(edit_id,))
    author=cur.fetchone()
    conn.close()
    return(author)

def saveAuthor(full_name,birthyear='',deathyear='',comment='', id=0):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    if id == 0:
        sql='insert into author(full_name,birthyear,deathyear,comment,entry_datetime,update_datetime) VALUES (?, ?,?,?,now(),now());'
        cur.execute(sql,(full_name,birthyear,deathyear,comment))
    else:
        sql='update author set update_datetime=now(),full_name = ?,birthyear =?,deathyear = ?,comment = ? where id = ?;'
        cur.execute(sql,(full_name,birthyear,deathyear,comment,id))
    a_id = cur.lastrowid
    conn.commit()
    conn.close()
    return(a_id)

def deleteAuthors(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    for id in delete_ids:
        sql='delete from author where id=?'
        cur.execute(sql,(id,))
        sql='delete ignore from associate_source_author where author_id=?'
        cur.execute(sql,(id,))
    conn.commit()
    conn.close()

def idFromFullNamesList(full_names):
    conn = get_db_connection()
    cur=conn.cursor()
    ids=[]
    for fullName in full_names:
        commitFlag=False
        sql='select id from author where full_name=?;'
        cur.execute(sql,(fullName,))
        id=cur.fetchone()
        if not id:
            sql='insert into author(full_name) values(?);'
            cur.execute(sql,(fullName,))
            id=cur.lastrowid
            commitFlag=True
        else:
            id=id[0]
        ids.append(id)
        if commitFlag:
            conn.commit()
    conn.close()
    return ids

def authorsStringFromNoteId(snippetId):
    conn=get_db_connection()
    cur=conn.cursor()
    sql='with atable as (with a as(select asa.source_id, GROUP_CONCAT(a.full_name order by full_name asc separator ", ") as authors from associate_source_author asa join author a on a.id=asa.author_id group by asa.source_id) select a.authors, s.title as title, s.id as source_id from source s left join a on a.source_id =s.id ) select atable.authors from associate_source_note asn left join atable on atable.source_id=asn.source_id where asn.note_id=?;'
    cur.execute(sql,(snippetId,))
    authors=cur.fetchone()
    if authors:
        return(authors[0])
    else:
        return('')
    
def alterAuthors(authors, sourceId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)        
    authorIds=[]
    if authors:
        for author in authors:
            author=author.strip()
            if author:
                sql="SELECT id from author where full_name=?;"
                cur.execute(sql,(author,))
                author_entry =cur.fetchone()
                if author_entry:
                    author_id =author_entry['id']
                    authorIds.append(author_id)
                else:
                    sql="INSERT INTO author(full_name) values (?);"
                    cur.execute(sql,(author,))
                    authorIds.append(cur.lastrowid)
                    conn.commit()
    conn.close()
    if sourceId != 0:
        asm.linkAuthorsToSource(sourceId,authorIds)