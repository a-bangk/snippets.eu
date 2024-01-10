import sys
import mariadb
from flask import current_app

def get_db_connection():
    try: 
        conn = mariadb.connect( 
            user=current_app.config["user"], 
            password=current_app.config["passwd"],
            host=current_app.config["host"], 
            port=int(current_app.config["port"]), 
            database=current_app.config["database"], 
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
     