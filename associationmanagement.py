from dbconnections import get_db_connection

def linkAuthorsToSource(sId,aIds):
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute(f'DELETE IGNORE from associate_source_author where source_id={sId};')
    for aId in aIds:
        cur.execute(f'INSERT IGNORE INTO associate_source_author(source_id,author_id) VALUES({sId},{aId});')
    conn.commit()
    conn.close()

def linkTagsToNote(nId,tIds):
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute(f'DELETE IGNORE from associate_notetag_note where note_id={nId};')
    for tId in tIds:
        cur.execute(f'INSERT IGNORE INTO associate_notetag_note(note_id,notetag_id) VALUES({nId},{tId});')
    conn.commit()
    conn.close()

def linkSourceToNote(nId,sId):
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute(f'DELETE IGNORE from associate_source_note where note_id={nId};')
    cur.execute(f'INSERT IGNORE INTO associate_source_note (source_id, note_id) VALUES ({sId}, {nId});')
    conn.commit()
    conn.close()