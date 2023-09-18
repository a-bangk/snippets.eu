from dbconnections import get_db_connection

def deleteTags(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    for id in delete_ids:
        cur.execute(f'delete from notetag where id={id}')
        cur.execute(f'delete from associate_notetag_note where notetag_id={id}')
    conn.commit()
    conn.close()


def listTagsFull():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('SELECT * from notetag order by id desc ;')
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
    return tags