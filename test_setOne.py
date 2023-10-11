
import authormanagement as am
import sourcemanagement as sm
import notemanagement as nm


def test_amIdFromFullNameList():
    assert am.idFromFullNamesList(["Milton Friedman","Finn Kjems","Gary Enzo","Carl Marx"]) == [112,3,2,160]

def test_smIdFromTitle():
    assert sm.idFromTitle("BabyWise") == 1
    print(id)

def test_sourceFunctions():
    sm.alterSource("Bob Smith", "Test Title 1", '',3,'http://www.google.com','')
    sId=sm.idFromTitleAndUrl("Test Title 1","http://www.google.com")
    sm.alterSource("Bob Smith", "Test Title 2", '2002',3,'http://www.google.com',sId)
    sm.deleteSource([sId])

def test_usingQuotes():
    sId=sm.idFromTitleAndUrl('"','"')
    sm.deleteSource([sId])