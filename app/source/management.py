from app.helperfunctions import get_db_connection, conn_alchemy
import app.authormanagement as am
import app.associationmanagement as asm
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

def dictSourceTypes():
    query = 'select id,entry from source_type st;'
    session = sessionmaker(bind=conn_alchemy())()
    result =session.execute(text(query))
    session.close()
    keys = result.keys()
    dictSourceTypes = [dict(zip(keys, row)) for row in result]
    return dictSourceTypes

def listSources():
    query = 'SELECT st.entry as type, s.id, s.title as title, GROUP_CONCAT(a.full_name SEPARATOR ", ") as author, a.id as a_id, s.url as url FROM source s LEFT JOIN associate_source_author aa ON s.id = aa.source_id LEFT JOIN author a ON aa.author_id = a.id LEFT JOIN source_type st ON s.source_type_id = st.id GROUP BY s.id ORDER BY s.id DESC;'
    session = sessionmaker(bind=conn_alchemy())()
    result =session.execute(text(query))
    session.close()
    keys = result.keys()
    sources_list = [dict(zip(keys, row)) for row in result]
    return sources_list

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
    session = sessionmaker(bind=conn_alchemy())()
    query=text('SELECT id from source where title = :title;')
    record = session.execute(query, {'title': title}).fetchone()
    if record:
        id=record[0]
    else:
        insert_query = text("INSERT INTO source (title, entry_datetime, update_datetime) VALUES (:title, NOW(), NOW())")
        session.execute(insert_query, {'title': title})
        session.flush()
        id = session.execute(text("SELECT LAST_INSERT_ID()")).scalar()
        session.commit()
    session.close()
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