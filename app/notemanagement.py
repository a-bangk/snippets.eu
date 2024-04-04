from urllib.parse import quote
import markdown

from .helperfunctions import get_db_connection
from . import associationmanagement as asm
from . import tagmanagement as tm
from .source import management as sm
from . import authormanagement as am

def list_notes_user_id_recent_14(userId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql_query='select * from snippet_view WHERE user_id = ? ORDER BY note_update_epoch DESC limit 14;'
    cur.execute(sql_query,(userId,))
    db_notes=cur.fetchall()
    conn.close()
    return snippets_result_enrichment(db_notes)

def tag_urls_from_tags(tag_list, username):
    tags_urls = []
    for tag in tag_list:
        tag=tag.strip()
        encoded_tag = quote(tag)
        tags_urls.append(f'<a href="/{username}/tag={encoded_tag}">{tag}</a>')
    return '; '.join(tags_urls)

def list_notes_epoch(id_list):
    conn = get_db_connection()
    placeholders = ', '.join(['%s'] * len(id_list))
    cur=conn.cursor(dictionary=True)
    sql_query=f'select * from snippet_view WHERE note_id in ({placeholders}) ORDER BY note_update_epoch DESC;'
    cur.execute(sql_query,id_list)
    db_notes=cur.fetchall()
    conn.close()
    return snippets_result_enrichment(db_notes)

def list_notes_for_userid_sourceid(user_id,source_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql_query='SELECT * FROM snippet_view WHERE user_id = ? AND source_id=? ORDER BY note_update_epoch DESC;'
    cur.execute(sql_query,(user_id,source_id))
    db_notes=cur.fetchall()
    conn.close()
    return snippets_result_enrichment(db_notes)

def list_note_for_user_id_deleted_source(user_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql_query='SELECT * FROM snippet_view WHERE user_id = ? AND source_id is NULL ORDER BY note_update_epoch DESC;'
    cur.execute(sql_query,(user_id,))
    db_notes=cur.fetchall()
    conn.close()
    return snippets_result_enrichment(db_notes)

def list_notes_for_user_id_tag(user_id, tag):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql_query="WITH nt AS ( SELECT ann.note_id, GROUP_CONCAT(DISTINCT nt.tag ORDER BY nt.tag ASC SEPARATOR '; ') AS tags, GROUP_CONCAT(DISTINCT nt.id ORDER BY nt.tag ASC SEPARATOR ';') as tagsId FROM associate_notetag_note ann JOIN notetag nt ON nt.id = ann.notetag_id WHERE ann.note_id IN ( SELECT distinct ann_inner.note_id FROM associate_notetag_note ann_inner JOIN notetag nt_inner ON nt_inner.id = ann_inner.notetag_id WHERE nt_inner.tag = ? ) GROUP BY ann.note_id ), s AS ( SELECT asn.note_id, GROUP_CONCAT(s.title SEPARATOR ', ') AS sources, s.id, s.url FROM associate_source_note asn JOIN source s ON s.id = asn.source_id GROUP BY asn.note_id ) SELECT n.id as note_id, s.id as source_id, n.content as content, n.update_epoch as note_update_epoch, nt.tags as tags, nt.tagsId as tagIds, s.sources as sources, s.url as url, u.username username, u.id as user_id FROM note n LEFT JOIN nt ON nt.note_id = n.id LEFT JOIN s ON s.note_id = n.id JOIN user u ON n.user_id = u.id where tags is not null and user_id=? order by note_update_epoch desc;"
    cur.execute(sql_query,(tag,user_id))
    db_notes=cur.fetchall()
    conn.close()
    return snippets_result_enrichment(db_notes)
  
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
        note["source_id"]=f'/{note.get("username")}/source={note.get("source_id")}'
        note["explore_source_url"]=note.pop("source_id")
        if note["tags"] is not None:
            note["explore_tag_urls"]=tag_urls_from_tags(note["tags"].split(";"), note.get("username"))
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

def add_new_snippet(content,user_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)   
    sql="insert into note(content,user_id,entry_epoch,update_epoch) VALUES (?, ?, UNIX_TIMESTAMP(now()), UNIX_TIMESTAMP(now()))"
    cur.execute(sql,(content,user_id))
    snippetId=cur.lastrowid
    conn.commit()
    conn.close()
    return(snippetId)

def update_snippet(content,snippetId):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    sql_query="update note set content = ?,update_epoch=UNIX_TIMESTAMP(now()) where id = ?;"   
    cur.execute(sql_query,(content,snippetId))
    conn.commit()
    conn.close()

def alter_snippet(content,source_title,tags,url,authors,snippet_id,user_id):
    if snippet_id == 'False':
        snippet_id=add_new_snippet(content,user_id)
    else:
        update_snippet(content,snippet_id)
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
    if source_title and authors[0] != '':
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

def snippetContent(snippet_id):
    conn = get_db_connection()
    cur=conn.cursor()
    sql="select content from note where id=?;"
    cur.execute(sql,(snippet_id,))
    content=cur.fetchone()[0]
    conn.close()
    return(content)

def snippets_result_enrichment(snippets_query_result):
    notes=[]
    for note in snippets_query_result:
        note['content_raw'] =note['content']
        note['content'] = markdown.markdown(note['content'])
        if note["sources"] is None:
            note["sources"] = "Source Deleted"
        note["explore_source_url"]=sm.generate_source_url_link(note.get("username"), note["sources"])
        if note["tags"] is not None:
            note["explore_tag_urls"]=tag_urls_from_tags(note["tags"].split(";"), note.get("username"))
        notes.append(note)
    return notes