import authormanagement as am

def test_amIdFromFullNameList():
    idList=am.idFromFullNamesList(["Milton Friedman","Finn Kjems","Gary Enzo","Carl Marx"])
    print(idList)

if __name__ == "__main__":
    test_amIdFromFullNameList()
    print("Tests Run")