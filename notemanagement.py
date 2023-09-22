from dbconnections import get_db_connection
import markdown
import re

def listNotes():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('with nt as ( select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR "; ") as tags  from associate_notetag_note ann  join notetag nt on nt.id = ann.notetag_id  group by ann.note_id ), s as ( select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources  from associate_source_note asn  join source s on s.id = asn.source_id  group by asn.note_id ) select n.id,n.content, n.entry_datetime,nt.tags,s.sources from note n left join nt on nt.note_id = n.id left join s on s.note_id = n.id order by n.id desc;')
    db_notes=cur.fetchall()
    conn.close()
    notes=[]
    for note in db_notes:
        note['content'] = markdown.markdown(note['content'])
        notes.append(note)
    return notes

def listTaggedNotes(tags,filter):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('with nt as ( select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR "; ") as tags  from associate_notetag_note ann  join notetag nt on nt.id = ann.notetag_id  group by ann.note_id ), s as ( select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources  from associate_source_note asn  join source s on s.id = asn.source_id  group by asn.note_id ) select n.id,n.content, n.entry_datetime,nt.tags,s.sources from note n left join nt on nt.note_id = n.id left join s on s.note_id = n.id order by n.id desc;')
    db_notes=cur.fetchall()
    conn.close()
    notes=[]
    for note in db_notes:
        if filter=="OR":
            if note['tags']:
                for tag in tags:
                    tag=tag.strip()
                    if tag in note['tags']:
                        note['content'] = markdown.markdown(note['content'])
                        notes.append(note)
        if filter=="AND":
            if note['tags']:
                tagPresent=True
                for tag in tags:
                    tag=tag.strip()
                    if tag not in note['tags']:
                        tagPresent=False
                if tagPresent:    
                    note['content'] = markdown.markdown(note['content'])
                    notes.append(note)
    return notes

def addNote(content,source,tags,url):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute(f'insert into note(content,entry_datetime) VALUES ("{content}", now())')
    n_id = cur.lastrowid
    tag_ids=[]
    for tag in tags:
        tag=tag.strip()
        if tag:
            cur.execute(f'SELECT id from notetag where tag="{tag}"')
            tag_entry =cur.fetchone()
            if tag_entry:
                tag_id =tag_entry['id']
                tag_ids.append(tag_id)
            else:
                cur.execute(f'INSERT INTO notetag (tag,entry_datetime,update_datetime) values ("{tag}", now(),now());')
                tag_ids.append(cur.lastrowid)
    for tag_id in tag_ids:
        cur.execute(f'INSERT INTO associate_notetag_note (notetag_id, note_id) VALUES ({tag_id}, {n_id});')
    
    if source:    
        cur.execute(f'SELECT id from source where title like"{source}%"')
        source_entry =cur.fetchone()
        if source_entry:
             source_id =source_entry['id']
        else:
            cur.execute(f'INSERT INTO source (title,entry_datetime,update_datetime) values ("{source}", now(),now());')
            source_id=cur.lastrowid
        cur.execute(f'INSERT INTO associate_source_note (source_id, note_id) VALUES ({source_id}, {n_id});')    

    if url:    
        cur.execute(f'SELECT id from source where url like"{url}%"')
        source_entry =cur.fetchone()
        if source_entry:
             source_id =source_entry['id']
        else:
            cur.execute(f'INSERT INTO source (url,entry_datetime,update_datetime) values ("{url}", now(),now());')
            source_id=cur.lastrowid
        cur.execute(f'INSERT INTO associate_source_note (source_id, note_id) VALUES ({source_id}, {n_id});')    
    conn.commit()
    conn.close()

def deleteSnippet(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    for id in delete_ids:
        cur.execute(f'delete from note where id={id}')
        cur.execute(f'delete from associate_notetag_note where note_id={id}')
    conn.commit()
    conn.close()

def editSnippet(edit_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute(f'select content from note where id={edit_id[0]}')
    cur.execute(f'update note set update_datetime=now() where id = {edit_id[0]};')
    conn.commit()
    note=cur.fetchall()
    print(note)
    conn.close()
