import os
import pymongo

client = pymongo.MongoClient()
db = client.leadvsgold
folderdb = db.folders


def listFolders():
    basedir = os.path.join('webapp', 'folders')
    dirlist = [d for d in os.listdir(basedir) if os.path.isdir(os.path.join(
        basedir, d))]
    return dirlist


def foldersToDb(dirlist):
    folderdb.insert_one({"folders":dirlist})

if __name__ == "__main__":
    folderdb.drop()
    dlist = listFolders()
    foldersToDb(dlist)
