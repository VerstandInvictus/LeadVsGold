import os
import shutil
import pymongo
from flask import Flask, send_file, request, Response, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient()
db = client.leadvsgold


def jsonWrapper(inputStructure, isCursor=1):
    if not request.is_xhr:
        indent = 4
    else:
        indent = None
    if isCursor == 1:
        outval = list(inputStructure)
    else:
        outval = inputStructure
    return Response(
        json.dumps(outval, indent=indent),
        mimetype='application/json')


def dbHandles(dbname, whichdb):
    initdbn = "init" + dbname
    fldbn = 'fileList' + dbname
    if whichdb == "fldb":
        return db[fldbn]
    if whichdb == "initdb":
        return db[initdbn]
    if whichdb == "cfgdb":
        return db[initdbn].find_one({'_id': "initDict"})


def currentIndex(dbname):
    return dbHandles(dbname, 'initdb').find_one({"_id": "index"})


def updateLocation(index, location, dbname):
    dbHandles(dbname, 'fldb').update_one(
        {"_id": index},
        {
            "$set": {
                "location": location
            }
        }
    )


def getCurFile(dbname):
    curFile = dbHandles(dbname, 'fldb').find_one(
        {"_id": currentIndex(dbname)["batch"]})
    if curFile is None:
        return dbHandles(dbname, 'cfgdb')["noneObject"]
    else:
        return curFile


def incrementIndex(num, dbname):
    dbHandles(dbname, 'initdb').update_one(
        {'_id': "index"},
        {
            "$set": {
                "batch": currentIndex(dbname)["batch"] + num,
                "session": currentIndex(dbname)["session"] + num
            }
        }
    )


def setIndex(num, dbname):
    dbHandles(dbname, 'initdb').update_one(
        {'_id': "index"},
        {
            "$set": {
                "batch": num,
            }
        }
    )


def resetSession(num, dbname):
    dbHandles(dbname, 'initdb').update_one(
        {'_id': "index"},
        {
            "$set": {
                "session": num
            }
        }
    )


def itemsRemain(dbname):
    files = os.listdir(dbHandles(dbname, 'cfgdb')['stackFolder'])
    return len(files)


@app.route('/folders')
def getFolders():
    return jsonWrapper(db.folders.find_one(), isCursor=0)


@app.route('/<dbname>/image/<nonce>')
def showFile(nonce, dbname):
    return send_file(getCurFile(dbname)["location"])


@app.route('/<dbname>/next/<action>/<nonce>')
def skipForward(action, nonce, dbname):
    curFile = getCurFile(dbname)
    if curFile == dbHandles(dbname, 'cfgdb')['noneObject']:
        setIndex(0, dbname)
        return send_file(dbHandles(dbname, 'cfgdb')['noneObject']["location"])
    newPath = os.path.join(dbHandles(
        dbname, 'cfgdb')['actions'][action], curFile["name"])
    if curFile['location'] != newPath:
        shutil.copy2(curFile['location'], newPath)
        os.remove(curFile['location'])
        updateLocation(currentIndex(dbname)['batch'], newPath, dbname)
    incrementIndex(1, dbname)
    return send_file(getCurFile(dbname)['location'])


@app.route('/<dbname>/imgtap')
def tapAction(dbname):
    curFile = getCurFile(dbname)
    newPath = os.path.join(dbHandles(
        dbname, 'cfgdb')['actions']['tap'], curFile['name'])
    shutil.copy2(curFile['location'], newPath)
    return "OK", 200


@app.route('/<dbname>/prev/<nonce>')
def skipBack(nonce, dbname):
    incrementIndex(-1, dbname)
    return send_file(getCurFile(dbname)['location'])


@app.route('/<dbname>/info/<nonce>')
def sendFolder(nonce, dbname):
    f = getCurFile(dbname)
    npath = f['location']
    curfile = os.path.split(npath)[0]
    folder = os.path.split(curfile)[1]
    creator = f['creator']
    mtime = f['mtime']
    retstring = ":".join((
        folder,
        creator,
        str(currentIndex(dbname)['batch']),
        str(currentIndex(dbname)['session']),
        str(itemsRemain(dbname)),
        mtime
    ))
    return retstring


@app.route('/<dbname>/info/reset')
def tapInfobox(dbname):
    resetSession(0, dbname)
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
