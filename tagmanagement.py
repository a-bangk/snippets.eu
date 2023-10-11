from dbconnections import get_db_connection

def deleteTags(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    for id in delete_ids:
        sql='delete from notetag where id=?;'
        cur.execute(sql,(id,))
        sql='delete from associate_notetag_note where notetag_id=?;'
        cur.execute(sql,(id,))
    conn.commit()
    conn.close()


def listTagsFull():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('SELECT * from notetag order by id desc;')
    db_tags=cur.fetchall()
    conn.close()
    tags=[]
    for tag in db_tags:
        tags.append(tag)
    return tags


def listTags():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('select tag from notetag;')
    db_tags=cur.fetchall()
    conn.close()
    tags=[]
    for tag in db_tags:
        tags.append(tag['tag'])
    tags=sorted(tags)
    return tags

def idFromTagsList(tagList):
    conn = get_db_connection()
    cur=conn.cursor()
    ids=[]
    for tag in tagList:
        commitFlag=False
        sql='select id from notetag where tag=?;'
        cur.execute(sql,(tag,))
        id=cur.fetchone()
        if not id:
            sql='insert into notetag(tag, entry_datetime, update_datetime) values(?,now(),now());'
            cur.execute(sql,(tag,))
            id=cur.lastrowid
            commitFlag=True
        else:
            id=id[0]
        ids.append(id)
        if commitFlag:
            conn.commit()        
    conn.close()
    return ids