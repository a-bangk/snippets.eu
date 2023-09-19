from dbconnections import get_db_connection

def listSources():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('select st.entry as type,s.id,s.title as title, GROUP_CONCAT(concat(IFNULL(a.title,"")," ",IFNULL(a.forename,""),IFNULL(a.middlename,"")," ",IFNULL(a.surname,""), " ",IFNULL(a.postnominal,"")) SEPARATOR " & ") as author,a.id as a_id, s.url as url from source s left join associate_source_author aa on s.id = aa.source_id left join author a on aa.author_id = a.id left join source_type st on s.source_type_id = st.id group by s.id order by s.id desc;')
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

def addSource(forename, surname, middlename, postnominal, author_title, source_title, year, sourceTypeId, url):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    if year=='':
        year = 'NULL'
    if url=='':
        url = 'NULL'
    insert_source_query=f'insert into source(title,entry_datetime,source_type_id,url,year) VALUES ("{source_title}", now(),"{sourceTypeId}", {url}, {year})'
    if forename or surname or middlename or  postnominal or author_title:
        cur.execute(f'insert into author(forename,surname,title,postnominal,middlename) VALUES ("{forename}","{surname}","{author_title}","{postnominal}","{middlename}")')
        a_id = cur.lastrowid
        cur.execute(insert_source_query)
        s_id = cur.lastrowid
        cur.execute(f'INSERT INTO associate_source_author (author_id, source_id) VALUES ({a_id}, {s_id});')
        conn.commit()
        conn.close()
    else:
        cur.execute(insert_source_query)
        conn.commit()
        conn.close()

def deleteSource(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    print(delete_ids)
    for id in delete_ids:
        cur.execute(f'delete from source where id={id}')
    conn.commit()
    conn.close()




