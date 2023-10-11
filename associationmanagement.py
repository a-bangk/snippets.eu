from dbconnections import get_db_connection

def linkAuthorsToSource(sId,aIds):
    print(type(sId))
    print(type(int(sId)))

    conn = get_db_connection()
    cur=conn.cursor()
    sql='DELETE IGNORE from associate_source_author where source_id=?;'
    cur.execute(sql,(sId,))
    for aId in aIds:
        sql='INSERT IGNORE INTO associate_source_author(source_id,author_id) VALUES(?,?);'
        cur.execute(sql,(sId,aId))
    conn.commit()
    conn.close()

def linkTagsToNote(nId,tIds):
    conn = get_db_connection()
    cur=conn.cursor()
    sql='DELETE IGNORE from associate_notetag_note where note_id=?;'
    cur.execute(sql,(nId,))
    for tId in tIds:
        sql='INSERT IGNORE INTO associate_notetag_note(note_id,notetag_id) VALUES(?,?);'
        cur.execute(sql,(nId,tId))
    conn.commit()
    conn.close()

def linkSourceToNote(nId,sId):
    conn = get_db_connection()
    cur=conn.cursor()
    sql='DELETE IGNORE from associate_source_note where note_id=?;'
    cur.execute(sql,(nId,))
    sql='INSERT IGNORE INTO associate_source_note (source_id, note_id) VALUES (?, ?);'
    cur.execute(sql,(nId,sId))
    conn.commit()
    conn.close()