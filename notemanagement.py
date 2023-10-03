from dbconnections import get_db_connection
import associationmanagement as asm
import tagmanagement as tm
import sourcemanagement as sm
import markdown

def listNotes():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('with nt as ( select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR "; ") as tags  from associate_notetag_note ann  join notetag nt on nt.id = ann.notetag_id  group by ann.note_id ), s as ( select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources, s.url  from associate_source_note asn  join source s on s.id = asn.source_id  group by asn.note_id ) select n.id,n.content, n.entry_datetime,nt.tags,s.sources, s.url from note n left join nt on nt.note_id = n.id left join s on s.note_id = n.id order by n.id desc;')
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

def addNewSnippet(content):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)   
    cur.execute(f'insert into note(content,entry_datetime) VALUES ("{content}", now())')
    snippetId=cur.lastrowid
    conn.commit()
    conn.close()
    return(snippetId)

def updateSnippet(content,snippetId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)   
    cur.execute(f'update note set content = "{content}",update_datetime=now() where id = "{snippetId}";')
    conn.commit()
    conn.close()

def alterSnippet(content,sourceTitle,tags,url,authors,snippetId):
    if snippetId == "False":
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
        addAuthors(authors,sId)  


def addAuthors(authors, sourceId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)        
    authorIds=[]
    if authors:
        for author in authors:
            author=author.strip()
            if author:
                cur.execute(f'SELECT id from author where full_name="{author}";')
                author_entry =cur.fetchone()
                if author_entry:
                    author_id =author_entry['id']
                    authorIds.append(author_id)
                else:
                    cur.execute(f'INSERT INTO author(full_name) values ("{author}");')
                    authorIds.append(cur.lastrowid)
        for authorId in authorIds:
            cur.execute(f'select exists(select * from associate_source_author where source_id={sourceId} and author_id={authorId});')
            cur.execute(f'INSERT INTO associate_source_author (source_id, author_id) VALUES ({sourceId}, {authorId});')
    conn.commit()
    conn.close()

def deleteSnippet(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    for id in delete_ids:
        id=int(id)
        cur.execute(f'delete from note where id={id};')
        cur.execute(f'delete IGNORE from associate_notetag_note where note_id={id};')
        cur.execute(f'delete IGNORE from associate_source_note where note_id={id};')
    conn.commit()
    conn.close()

def editSnippet(edit_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute(f'with nt as ( select ann.note_id, GROUP_CONCAT(nt.tag SEPARATOR ", ") as tags from associate_notetag_note ann join notetag nt on nt.id = ann.notetag_id group by ann.note_id ), s as ( select asn.note_id, GROUP_CONCAT(s.title SEPARATOR ", ") as sources, s.url from associate_source_note asn join source s on s.id = asn.source_id group by asn.note_id ) select n.id,n.content, n.entry_datetime,nt.tags,s.sources,s.url from note n left join nt on nt.note_id = n.id left join s on s.note_id = n.id where n.id={edit_id[0]};')
    previousSnippet=cur.fetchone()
    conn.close()
    return(previousSnippet)

def deleteAssociateLinks(delete_ids):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    for id in delete_ids:
        cur.execute(f'delete ignore from associate_notetag_note where note_id={id};')
        cur.execute(f'delete ignore from associate_source_note where note_id={id};')
    conn.commit()
    conn.close()
