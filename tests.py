import authormanagement as am
import sourcemanagement as sm


def test_amIdFromFullNameList():
    idList=am.idFromFullNamesList(["Milton Friedman","Finn Kjems","Gary Enzo","Carl Marx"])

def test_smIdFromTitle():
    id=sm.idFromTitle("BabyWise")
    print(id)

def test_amAuthorsListFromNoteId():
    authors=am.authorsListFromNoteId(46)
    print(type(authors[0]))

if __name__ == "__main__":
    test_smIdFromTitle()
    test_amAuthorsListFromNoteId()