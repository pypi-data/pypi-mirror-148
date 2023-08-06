import pymongo


def database_access():
    client = pymongo.MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
    database = client['DMS']
    return database
