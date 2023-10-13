from helperfunctions import get_db_connection
import associationmanagement as asm
import tagmanagement as tm
import sourcemanagement as sm
import authormanagement as am
import markdown

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
    return notes

def listTaggedNotes(tags,filter):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('with nt as ( select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR "; ") as tags  from associate_notetag_note ann  join notetag nt on nt.id = ann.notetag_id  group by ann.note_id ), s as ( select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources  from associate_source_note asn  join source s on s.id = asn.source_id  group by asn.note_id ) select n.id,n.content, n.entry_datetime,nt.tags,s.sources from note n left join nt on nt.note_id = n.id left join s on s.note_id = n.id order by n.update_datetime desc;')
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

def addNewSnippet(content):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)   
    sql="insert into note(content,entry_datetime,update_datetime) VALUES (?, now(), now())"
    cur.execute(sql,(content,))
    snippetId=cur.lastrowid
    conn.commit()
    conn.close()
    return(snippetId)

def updateSnippet(content,snippetId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql="update note set content = ?,update_datetime=now() where id = ?;"   
    cur.execute(sql,(content,snippetId))
    conn.commit()
    conn.close()

def alterSnippet(content,sourceTitle,tags,url,authors,snippetId):
    if snippetId == 'False':
        snippetId=addNewSnippet(content)
    else:
        updateSnippet(content,snippetId)
        deleteAssociateLinks(snippetId)
    if tags:
        tagIds=tm.idFromTagsList(tags)
        asm.linkTagsToNote(snippetId,tagIds)
    if sourceTitle and url:
        sId=sm.idFromTitleAndUrl(sourceTitle,url)
        asm.linkSourceToNote(snippetId,sId)
    elif sourceTitle:    
        sId=sm.idFromTitle(sourceTitle)
        asm.linkSourceToNote(snippetId,sId)
    elif url:    
        sId=sm.idFromUrl(url)
        asm.linkSourceToNote(snippetId,sId)
    #TODO Snip-94
    if (url or sourceTitle) and authors[0] != '':
        am.alterAuthors(authors,sId)  


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