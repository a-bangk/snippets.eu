import sys
import mariadb
from dynaconf import settings

def get_db_connection(): 
    print("hllow")
    print(settings.MYSQL)
    try: 
        conn = mariadb.connect( 
            user=settings.MYSQL.user, 
            password=settings.MYSQL.auth.get('passwd'), 
            host=settings.MYSQL.host, 
            port=settings.MYSQL.port, 
            database=settings.MYSQL.database 
        ) 
    except mariadb.Error as e: 
            print(f"Error connecting to MariaDB Platform: {e}") 
            sys.exit(1) 
    return conn 

def commaStringToList(commaString):
    itemList=commaString.split(',')
    itemList = [item.strip() for item in itemList]
    while("" in itemList):
        itemList.remove("")
    itemList = sorted(itemList, key=str.casefold)
    return itemList
     