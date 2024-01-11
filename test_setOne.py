
from app import authormanagement as am
from app.source import management as sm
from app import notemanagement as nm
from app import tagmanagement as tm
from app import helperfunctions as hf
from snippets import create_app
import pytest
from sqlalchemy import text

@pytest.fixture
def app():
    app=create_app()
    with app.app_context():
        yield app

def test_databaseConnection(app):
    db=hf.get_db_connection().database
    assert db == 'snippetsdb_testa'

def test_databaseConnectionAlchemy(app):
    result=hf.conn_alchemy().execute(text("SELECT DATABASE()"))
    db=result.scalar()
    assert db == 'snippetsdb_testa'

def test_amidFromFullNameList(app):
    assert am.idFromFullNamesList(["Milton Friedman","Finn Kjems","Gary Enzo","Karl Marx"]) == [71,72,73,74]

def test_smidFromTitle(app):
    assert sm.idFromTitle("BabyWise") == 61


# This test alters the database and therefore removed until fixed
#def test_sourceFunctions(app):
#    sm.alterSource("Bob Smith", "Test Title 1", '2000',3,'http://www.google.com','')
#    sId=sm.idFromTitleAndUrl("Test Title 1","http://www.google.com")
#    sm.alterSource("Bob Smith", "Test Title 2", '2002',3,'http://www.google.com',sId)
#    sm.deleteSource([sId])

def test_usingQuotes(app):
    sId=sm.idFromTitleAndUrl('"','"')
    sm.deleteSource([sId])

def test_alterSnippet_SourceTitle(app):
    content="Test Content 667504ggyj"
    nm.alterSnippet(content,"New title 3",'','',[''],'False')        
    sIds=nm.idsFromContent(content)
    latestId=sIds[0][0]
    sValues=nm.editSnippet(latestId)
    nm.deleteSnippet([latestId])
    sm.deleteSource([sm.idFromTitle("New title 3")])
    assert sValues["content"]==content
    assert sValues["sources"]=="New title 3"
    assert sValues["id"]==latestId

def test_alterSnippet_Tag(app):
    content="Test Content adding Tags"
    tagString="test tag,    testtag    ,  @dae ,   "
    tagList=hf.commaStringToList(tagString)
    nm.alterSnippet(content,'',tagList,'',[''],'False')        
    sIds=nm.idsFromContent(content)
    latestId=sIds[0][0]
    sValues=nm.editSnippet(latestId)
    nm.deleteSnippet([latestId])
    tm.deleteTagsById(tm.idFromTagsList(tagList))
    assert sValues["content"]==content
    assert sValues["tags"]=="@dae, test tag, testtag"
    assert sValues["id"]==latestId

def test_alterSnippet_All(app):
    startCount=len(nm.listNotes())
    content="Test Content adding All"
    title='Source with Authors'
    url="www.AWESOME-TEST.org     "
    tagString="test tag,    testtag    ,  @dae ,   "
    authorsString="Author 1,     Author person 3, M.D manpanfan,    "
    tagList=hf.commaStringToList(tagString)
    authorsList=hf.commaStringToList(authorsString)
    nm.alterSnippet(content,title,tagList,url,authorsList,'False')        
    sIds=nm.idsFromContent(content)
    latestId=sIds[0][0]
    allSnippets=nm.listNotes()
    assert startCount<len(allSnippets)
    sValues=allSnippets[000]
    authorsInDb=am.authorsStringFromNoteId(latestId)
    nm.deleteSnippet([latestId])
    tm.deleteTagsById(tm.idFromTagsList(tagList))
    authorIds=am.idFromFullNamesList(authorsList)
    am.deleteAuthors(authorIds)
    sourceId=sm.idFromTitleAndUrl(title,url)
    sm.deleteSource([sourceId])
    assert sValues["content"]=='<p>'+content+'</p>'
    assert sValues["tags"]=='@dae; test tag; testtag'
    assert sValues["id"]==latestId
    assert sValues["sources"]==title
    assert authorsInDb=="Author 1, Author person 3, M.D manpanfan"


# Functions remade to use SQLAlchemy
def test_smdictSourceTypes(app):
    result=sm.dictSourceTypes()
    assert result ==[{'id': 1, 'entry': 'fiction book'}, {'id': 2, 'entry': 'nonfiction book'}, {'id': 3, 'entry': 'video'}, {'id': 4, 'entry': 'hearsay'}, {'id': 5, 'entry': 'lecture'}, {'id': 6, 'entry': 'website'}, {'id': 7, 'entry': 'other'}, {'id': 8, 'entry': 'magazine'}]

def test_smlistSources(app):
    result=sm.listSources()[0]
    print(result)
    assert result == {'type': None, 'id': 61, 'title': 'BabyWise', 'author': None, 'a_id': None, 'url': None}

## Test Endpoints

def test_endpoint_filter(app):
    with app.test_client() as client:
        response = client.get('/filtersnippetslist')
        assert response.status_code == 200

def test_endpoint_source(app):
    with app.test_client() as client:
        response = client.get('/source')
        assert response.status_code == 200


def test_endpoint_author(app):
    with app.test_client() as client:
        response = client.get('/author')
        assert response.status_code == 200


def test_endpoint_tag(app):
    with app.test_client() as client:
        response = client.get('/tag')
        assert response.status_code == 200

    
def test_endpoint_about(app):
    with app.test_client() as client:
        response = client.get('/about')
        assert response.status_code == 200