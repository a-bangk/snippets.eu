from .helperfunctions import get_db_connection


def deleteTagsById(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    for id in delete_ids:
        sql='delete from notetag where id=?;'
        cur.execute(sql,(id,))
        sql='delete from associate_notetag_note where notetag_id=?;'
        cur.execute(sql,(id,))
    conn.commit()
    conn.close()


def addTagForUser(tag,user_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql_query='insert into notetag(tag,user_id, entry_datetime, update_datetime) VALUES (?, ?, now(), now())'
    cur=conn.cursor(dictionary=True)
    cur.execute(sql_query,(tag,user_id))
    conn.commit()
    conn.close()

def tagsForUserId(user_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql_query='select tag from notetag where user_id=?;'
    cur.execute(sql_query,(user_id,))
    db_tags=cur.fetchall()
    conn.close()
    tags=[]
    for tag in db_tags:
        tags.append(tag['tag'])
    tags=sorted(tags,key=str.casefold)
    return tags


def tagsAllFieldsForUserId(user_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql_query='SELECT * from notetag where user_id=? order by id desc;'
    cur.execute(sql_query,(user_id,))
    db_tags=cur.fetchall()
    conn.close()
    tags=[]
    for tag in db_tags:
        tags.append(tag)
    return tags

def idFromTagsList(tag_list,user_id):
    conn = get_db_connection()
    cur=conn.cursor()
    ids=[]
    for tag in tag_list:
        commitFlag=False
        sql='select id from notetag where tag=? and user_id=?;'
        cur.execute(sql,(tag,user_id))
        id=cur.fetchone()
        if not id:
            sql='insert into notetag(tag, entry_datetime, update_datetime, user_id) values(?,now(),now(), ?);'
            cur.execute(sql,(tag,user_id))
            id=cur.lastrowid
            commitFlag=True
        else:
            id=id[0]
        ids.append(id)
        if commitFlag:
            conn.commit()        
    conn.close()
    return ids