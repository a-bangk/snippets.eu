import sys
import mariadb
from sqlalchemy import create_engine, text
import pymysql
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

def conn_alchemy():
    engine = create_engine('mysql+pymysql://'+current_app.config["user"]+':'+current_app.config["passwd"]+'@'+current_app.config["host"]+':'+current_app.config["port"]+'/'+current_app.config["database"], pool_recycle=3600, echo=True)
    return engine.connect()

def commaStringToList(commaString):
    itemList=commaString.split(',')
    itemList = [item.strip() for item in itemList]
    while("" in itemList):
        itemList.remove("")
    itemList = sorted(itemList, key=str.casefold)
    return itemList
     