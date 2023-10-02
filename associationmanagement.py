from dbconnections import get_db_connection

def sourceAuthor(sId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute(f'select * from associate_source_author where source_id={sId}')
    rows=cur.fetchall()
    conn.close()
    return(rows)

def linkAuthorsToSource(sId,aIds):
    conn = get_db_connection()
    cur=conn.cursor()
    for aId in aIds:
        cur.execute(f'INSERT IGNORE INTO associate_source_author(source_id,author_id) VALUES({sId},{aId});')
    conn.commit()
    conn.close()
