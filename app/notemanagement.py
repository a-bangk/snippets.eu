from .helperfunctions import get_db_connection
from . import associationmanagement as asm
from . import tagmanagement as tm
from .source import management as sm
from . import authormanagement as am
import markdown

""" 
def listNotes():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('with nt as ( select ann.note_id, GROUP_CONCAT(nt.tag order by tag asc SEPARATOR "; ") as tags  from associate_notetag_note ann  join notetag nt on nt.id = ann.notetag_id  group by ann.note_id ), s as ( select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources, s.url  from associate_source_note asn  join source s on s.id = asn.source_id  group by asn.note_id ) select n.id,n.content, n.entry_datetime,nt.tags,s.sources, s.url from note n left join nt on nt.note_id = n.id left join s on s.note_id = n.id order by n.update_datetime desc;')
    db_notes=cur.fetchall()
    conn.close()
    notes=[]
    for note in db_notes:
        note['content'] = markdown.markdown(note['content'])
        notes.append(note)
    return notes """

def listNotesForUserId(user_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql_query='WITH nt AS ( SELECT ann.note_id, GROUP_CONCAT(nt.tag ORDER BY tag ASC SEPARATOR "; ") AS tags FROM associate_notetag_note ann JOIN notetag nt ON nt.id = ann.notetag_id GROUP BY ann.note_id ), s AS ( SELECT asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") AS sources,s.id, s.url FROM associate_source_note asn JOIN source s ON s.id = asn.source_id GROUP BY asn.note_id ) SELECT n.id,s.id as source_id, n.content, n.entry_datetime, nt.tags, s.sources, s.url, u.username FROM note n LEFT JOIN nt ON nt.note_id = n.id LEFT JOIN s ON s.note_id = n.id JOIN user u ON n.user_id = u.id WHERE n.user_id = ? ORDER BY n.update_datetime DESC;'
    cur.execute(sql_query,(user_id,))
    db_notes=cur.fetchall()
    conn.close()
    notes=[]
    for note in db_notes:
        note['content'] = markdown.markdown(note['content'])
        note["source_id"]=f'/{note.get("username")}/source={note.get("source_id")}'
        note["explore_source_url"]=note.pop("source_id")
        notes.append(note)
    return notes

def listNotes(id_list):
    conn = get_db_connection()
    placeholders = ', '.join(['%s'] * len(id_list))
    cur=conn.cursor(dictionary=True)
    sql_query=f'WITH nt AS ( SELECT ann.note_id, GROUP_CONCAT(nt.tag ORDER BY tag ASC SEPARATOR "; ") AS tags FROM associate_notetag_note ann JOIN notetag nt ON nt.id = ann.notetag_id GROUP BY ann.note_id ), s AS ( SELECT asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") AS sources,s.id, s.url FROM associate_source_note asn JOIN source s ON s.id = asn.source_id GROUP BY asn.note_id ) SELECT n.id, n.content, n.entry_datetime, nt.tags, s.id as source_id,s.sources, s.url, u.username FROM note n LEFT JOIN nt ON nt.note_id = n.id LEFT JOIN s ON s.note_id = n.id JOIN user u ON n.user_id = u.id WHERE n.id in ({placeholders}) ORDER BY n.update_datetime DESC;'
    cur.execute(sql_query,id_list)
    db_notes=cur.fetchall()
    conn.close()
    notes=[]
    for note in db_notes:
        note['content'] = markdown.markdown(note['content'])
        note["source_id"]=f'/{note.get("username")}/source={note.get("source_id")}'
        note["explore_source_url"]=note.pop("source_id")
        notes.append(note)
    return notes

def listNotesWithExplore(id_list):
    conn = get_db_connection()
    placeholders = ', '.join(['%s'] * len(id_list))
    cur=conn.cursor(dictionary=True)
    sql_query=f'WITH nt AS ( SELECT ann.note_id, GROUP_CONCAT(nt.tag ORDER BY tag ASC SEPARATOR "; ") AS tags FROM associate_notetag_note ann JOIN notetag nt ON nt.id = ann.notetag_id GROUP BY ann.note_id ), s AS ( SELECT asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") AS sources,s.id, s.url FROM associate_source_note asn JOIN source s ON s.id = asn.source_id GROUP BY asn.note_id ) SELECT n.id, n.content, n.entry_datetime, nt.tags, s.id as source_id,s.sources, s.url, u.username FROM note n LEFT JOIN nt ON nt.note_id = n.id LEFT JOIN s ON s.note_id = n.id JOIN user u ON n.user_id = u.id WHERE n.id in ({placeholders}) ORDER BY n.update_datetime DESC;'
    cur.execute(sql_query,id_list)
    db_notes=cur.fetchall()
    conn.close()
    notes=[]
    for note in db_notes:
        note['content'] = markdown.markdown(note['content'])
        note['exploreSource'] = f"/{note['username']}/source={note['source_id']}"
        notes.append(note)
    return notes


def listNotesForUserIdSourceId(user_id,source_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql_query='WITH nt AS ( SELECT ann.note_id, GROUP_CONCAT(nt.tag ORDER BY tag ASC SEPARATOR "; ") AS tags FROM associate_notetag_note ann JOIN notetag nt ON nt.id = ann.notetag_id GROUP BY ann.note_id ), s AS ( SELECT asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") AS sources,s.id, s.url FROM associate_source_note asn JOIN source s ON s.id = asn.source_id GROUP BY asn.note_id ) SELECT n.id, n.content, n.entry_datetime, nt.tags, s.sources, s.url, u.username FROM note n LEFT JOIN nt ON nt.note_id = n.id LEFT JOIN s ON s.note_id = n.id JOIN user u ON n.user_id = u.id WHERE n.user_id = ? and s.id=? ORDER BY n.update_datetime DESC;'
    cur.execute(sql_query,(user_id,source_id))
    db_notes=cur.fetchall()
    conn.close()
    notes=[]
    for note in db_notes:
        note['content'] = markdown.markdown(note['content'])
        notes.append(note)
    return notes

def listNotesForNoteIdsSourceIds(id_list, source_list):
    conn = get_db_connection()
    placeholders = ', '.join(['%s'] * len(id_list))
    source_ids=', '.join(['%s'] * len(source_list))
    cur=conn.cursor(dictionary=True)
    sql_query='WITH nt AS ( SELECT ann.note_id, GROUP_CONCAT(nt.tag ORDER BY tag ASC SEPARATOR "; ") AS tags FROM associate_notetag_note ann JOIN notetag nt ON nt.id = ann.notetag_id GROUP BY ann.note_id ), s AS ( SELECT asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") AS sources,s.id, s.url FROM associate_source_note asn JOIN source s ON s.id = asn.source_id GROUP BY asn.note_id ) SELECT n.id, n.content, n.entry_datetime, nt.tags, s.sources, s.url, u.username FROM note n LEFT JOIN nt ON nt.note_id = n.id LEFT JOIN s ON s.note_id = n.id JOIN user u ON n.user_id = u.id WHERE n.id in ({placeholders}) and s.id in ({source_ids}) ORDER BY n.update_datetime DESC;'
    cur.execute(sql_query,(placeholders,source_ids))
    db_notes=cur.fetchall()
    conn.close()
    notes=[]
    for note in db_notes:
        note['content'] = markdown.markdown(note['content'])
        notes.append(note)
    return notes

def listNotesForNoteIdsSourceId(id_list, source_id):
    conn = get_db_connection()
    placeholders = ', '.join(['%s'] * len(id_list))
    cur=conn.cursor(dictionary=True)
    sql_query='WITH nt AS ( SELECT ann.note_id, GROUP_CONCAT(nt.tag ORDER BY tag ASC SEPARATOR "; ") AS tags FROM associate_notetag_note ann JOIN notetag nt ON nt.id = ann.notetag_id GROUP BY ann.note_id ), s AS ( SELECT asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") AS sources,s.id, s.url FROM associate_source_note asn JOIN source s ON s.id = asn.source_id GROUP BY asn.note_id ) SELECT n.id, n.content, n.entry_datetime, nt.tags, s.sources, s.url, u.username FROM note n LEFT JOIN nt ON nt.note_id = n.id LEFT JOIN s ON s.note_id = n.id JOIN user u ON n.user_id = u.id WHERE n.id in ({placeholders}) and s.id=%s ORDER BY n.update_datetime DESC;'
    cur.execute(sql_query,(placeholders,source_id))
    db_notes=cur.fetchall()
    conn.close()
    notes=[]
    for note in db_notes:
        note['content'] = markdown.markdown(note['content'])
        notes.append(note)
    return notes

def listTaggedNotesForUserId(tags,filter,user_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql_query='with nt as ( select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR "; ") as tags  from associate_notetag_note ann  join notetag nt on nt.id = ann.notetag_id  group by ann.note_id ), s as ( select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources  from associate_source_note asn  join source s on s.id = asn.source_id  group by asn.note_id ) select n.id,n.content, n.entry_datetime,nt.tags,s.sources from note n left join nt on nt.note_id = n.id left join s on s.note_id = n.id where n.user_id=? order by n.update_datetime desc;'
    cur.execute(sql_query,(user_id,))
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

def addNewSnippet(content,user_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)   
    sql="insert into note(content,user_id,entry_datetime,update_datetime) VALUES (?, ?, now(), now())"
    cur.execute(sql,(content,user_id))
    snippetId=cur.lastrowid
    conn.commit()
    conn.close()
    return(snippetId)

def updateSnippet(content,snippetId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql_query="update note set content = ?,update_datetime=now() where id = ?;"   
    cur.execute(sql_query,(content,snippetId))
    conn.commit()
    conn.close()

def alterSnippet(content,source_title,tags,url,authors,snippet_id,user_id):
    if snippet_id == 'False':
        snippet_id=addNewSnippet(content,user_id)
    else:
        updateSnippet(content,snippet_id)
        deleteAssociateLinks(snippet_id)
    if tags:
        tagIds=tm.idFromTagsList(tags,user_id)
        asm.linkTagsToNote(snippet_id,tagIds)
    if source_title and url:
        source_id=sm.idFromTitleAndUrl(source_title,url,user_id)
        asm.linkSourceToNote(snippet_id,source_id)
    elif source_title:    
        source_id=sm.idFromTitle(source_title,user_id)
        asm.linkSourceToNote(snippet_id,source_id)
    elif url:    
        source_id=sm.idFromUrl(url)
        asm.linkSourceToNote(snippet_id,source_id)
    #TODO Snip-94
    if (url or source_title) and authors[0] != '':
        am.alterAuthors(authors,source_id,user_id)  


def deleteSnippet(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    for id in delete_ids:
        id=int(id)
        sql="delete from note where id=?;"
        cur.execute(sql,(id,))
        sql="delete IGNORE from associate_notetag_note where note_id=?;"
        cur.execute(sql,(id,))
        sql="delete IGNORE from associate_source_note where note_id=?;"
        cur.execute(sql,(id,))
    conn.commit()
    conn.close()

def editSnippet(edit_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql='with nt as ( select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR ", ") as tags from associate_notetag_note ann join notetag nt on nt.id = ann.notetag_id group by ann.note_id ), s as ( select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources, s.url from associate_source_note asn join source s on s.id = asn.source_id group by asn.note_id ) select n.id,n.content, n.entry_datetime,nt.tags,s.sources,s.url from note n left join nt on nt.note_id = n.id left join s on s.note_id = n.id where n.id=?;'
    cur.execute(sql,(edit_id,))
    previousSnippet=cur.fetchone()
    conn.close()
    return(previousSnippet)

def deleteAssociateLinks(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    for id in delete_ids:
        sql='delete ignore from associate_notetag_note where note_id=?;'
        cur.execute(sql,(id,))
        sql='delete ignore from associate_source_note where note_id=?;'
        cur.execute(sql,(id,))
    conn.commit()
    conn.close()

def idsFromContent(content):
    conn = get_db_connection()
    cur=conn.cursor()
    sql="SELECT id from note where content=? order by update_datetime desc;"
    cur.execute(sql,(content,))
    ids=cur.fetchall()
    conn.close()
    return(ids)