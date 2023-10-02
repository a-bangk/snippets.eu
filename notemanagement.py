from dbconnections import get_db_connection
import markdown

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

#Snip-92
def alterSnippet(content,source,tags,url,authors,snippetId):
    if snippetId == "False":
        snippetId=addNewSnippet(content)
    else:
        updateSnippet(content,snippetId)
        deleteAssociateLinks(snippetId)
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)    
    tag_ids=[]
    if tags:
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
            cur.execute(f'INSERT INTO associate_notetag_note (notetag_id, note_id) VALUES ({tag_id}, {snippetId});')
    if source:    
        cur.execute(f'SELECT id from source where title like"{source}%"')
        sourceEntry =cur.fetchone()
        if sourceEntry:
             sourceId =sourceEntry['id']
        else:
            cur.execute(f'INSERT INTO source (title,entry_datetime,update_datetime) values ("{source}", now(),now());')
            sourceId=cur.lastrowid
        cur.execute(f'INSERT INTO associate_source_note (source_id, note_id) VALUES ({sourceId}, {snippetId});')
    if url:    
        cur.execute(f'SELECT id from source where url like"{url}%"')
        source_entry =cur.fetchone()
        if source_entry:
             sourceId =source_entry['id']
        else:
            cur.execute(f'INSERT INTO source (url,entry_datetime,update_datetime) values ("{url}", now(),now());')
            sourceId=cur.lastrowid
        cur.execute(f'INSERT INTO associate_source_note (source_id, note_id) VALUES ({sourceId}, {snippetId});')  
    conn.commit()
    conn.close()
    #TODO Snip-94
    if (url or source) and authors[0] != '':
        addAuthors(authors,snippetId)  


def addAuthors(authors, sourceId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)        
    authorIds=[]
    if authors:
        for author in authors:
            author=author.strip()
            if author:
                cur.execute(f'SELECT id from author where full_name="{author}"')
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
        cur.execute(f'delete from note where id={id}')
        cur.execute(f'delete from associate_notetag_note where note_id={id}')
        cur.execute(f'delete from associate_source_note where note_id={id}')
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
        cur.execute(f'delete from associate_notetag_note where note_id={id}')
        cur.execute(f'delete from associate_source_note where note_id={id}')
    conn.commit()
    conn.close()
