from dbconnections import get_db_connection
import authormanagement as am
import associationmanagement as asm

def listSources():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('select st.entry as type,s.id,s.title as title, GROUP_CONCAT(a.full_name SEPARATOR " & ") as author,a.id as a_id, s.url as url from source s left join associate_source_author aa on s.id = aa.source_id left join author a on aa.author_id = a.id left join source_type st on s.source_type_id = st.id group by s.id order by s.id desc;')
    db_sources=cur.fetchall()
    conn.close()
    sources=[]
    for source in db_sources:
        sources.append(source)
    return sources

def listAuthors():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=False)
    cur.execute('select full_name as author from author;')
    authors_db=cur.fetchall()
    conn.close()
    authors=[]
    for author in authors_db:
        authors.append(author[0])
    return authors

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
        year = 'NULL'
    if url=='':
        url = 'NULL'
    if sId == "":
        sId=addSource(title,typeId,url,year)
    else:
        updateSource(title,url,typeId,year,sId)
    authorIds=am.idFromFullNamesList(authorFullNameList)
    asm.linkAuthorsToSource(sId,authorIds)

def deleteSource(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    for id in delete_ids:
        cur.execute(f'delete from source where id={id};')
        cur.execute(f'delete ignore from associate_source_note where source_id={id};')
        cur.execute(f'delete ignore from associate_source_author where source_id={id};')
    conn.commit()
    conn.close()

def loadSource(edit_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute(f'select st.entry as type,s.id,s.year as year, s.title as title, GROUP_CONCAT(a.full_name SEPARATOR " & ") as author, s.url as url from source s left join associate_source_author aa on s.id = aa.source_id left join author a on aa.author_id = a.id left join source_type st on s.source_type_id = st.id where s.id={edit_id};')
    previousSnippet=cur.fetchone()
    conn.close()
    return(previousSnippet)

def addSource(title, typeId, url, year):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute(f'insert into source(title,entry_datetime,source_type_id,url,year) VALUES ("{title}", now(),"{typeId}", "{url}", {year});')
    sId = cur.lastrowid
    conn.commit()
    conn.close()
    return(sId)

def linkAuthor(sourceId, authorId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute(f'INSERT INTO associate_source_author (author_id, source_id) VALUES ({authorId}, {sourceId});')
    conn.close()

def updateSource(title,url,typeId,year,sourceId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute(f'update source set title = "{title}",update_datetime=now(),url="{url}", source_type_id={typeId}, year={year} where id = "{sourceId}";')
    conn.commit()
    conn.close()

def idFromTitle(title):
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute(f'SELECT id from source where title = "{title}";')
    id=cur.fetchone()
    if not id:
        cur.execute(f'INSERT INTO source (title,entry_datetime,update_datetime) values ("{title}", now(),now());')
        id=cur.lastrowid
        conn.commit()
    else:
        id=id[0]     
    conn.close()
    return id

def idFromUrl(url):
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute(f'SELECT id from source where url = "{url}";')
    id=cur.fetchone()
    if not id:
        cur.execute(f'INSERT INTO source (url,entry_datetime,update_datetime) values ("{url}", now(),now());')
        id=cur.lastrowid
        conn.commit()
    else:
        id=id[0]     
    conn.close()
    return id

def idFromTitleAndUrl(title,url):
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute(f'SELECT id from source where title = "{title}" and url="{url}";')
    id=cur.fetchone()
    if not id:
        cur.execute(f'INSERT INTO source (title,entry_datetime,update_datetime,url) values ("{title}", now(),now(),"{url}");')
        id=cur.lastrowid
        conn.commit()
    else:
        id=id[0]     
    conn.close()
    return id