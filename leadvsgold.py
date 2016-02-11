import os
import shutil
import pymongo
from flask import Flask, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = pymongo.MongoClient()
db = client.leadvsgold
initdb = db.init
fldb = db.fileList
cfgDB = initdb.find_one({'_id': "initDict"})


def currentIndex():
    return initdb.find_one({"_id": "index"})


def updateLocation(index, location):
    fldb.update_one(
        {"_id": index},
        {
            "$set": {
                "location": location
            }
        }
    )


def getCurFile():
    curFile = fldb.find_one({"_id": currentIndex()["batch"]})
    if curFile is None:
        return cfgDB["noneObject"]
    else:
        return curFile


def incrementIndex(num):
    initdb.update_one(
        {'_id': "index"},
        {
            "$set": {
                "batch": currentIndex()["batch"] + num,
                "session": currentIndex()["session"] + num
            }
        }
    )


def setIndex(num):
    initdb.update_one(
        {'_id': "index"},
        {
            "$set": {
                "batch": num,
            }
        }
    )


def resetSession(num):
    initdb.update_one(
        {'_id': "index"},
        {
            "$set": {
                "session": num
            }
        }
    )


def itemsRemain():
    return fldb.count()


@app.route('/image/<nonce>')
def showFile(nonce):
    return send_file(getCurFile()["location"])


@app.route('/next/<action>/<nonce>')
def skipForward(action, nonce):
    curFile = getCurFile()
    if curFile == cfgDB['noneObject']:
        setIndex(0)
        return send_file(cfgDB.noneObject["location"])
    newPath = os.path.join(cfgDB['actions'][action], curFile["name"])
    if curFile['location'] != newPath:
        shutil.copy2(curFile['location'], newPath)
        os.remove(curFile['location'])
        updateLocation(currentIndex()['batch'], newPath)
    incrementIndex(1)
    return send_file(getCurFile()['location'])


@app.route('/imgtap')
def tapAction():
    curFile = getCurFile()
    newPath = os.path.join(cfgDB['actions']['tap'], curFile['name'])
    shutil.copy2(curFile['location'], newPath)
    return "OK", 200


@app.route('/prev/<nonce>')
def skipBack(nonce):
    incrementIndex(-1)
    return send_file(getCurFile()['location'])


@app.route('/info/<nonce>')
def sendFolder(nonce):
    npath = getCurFile()['location']
    curfile = os.path.split(npath)[0]
    folder = os.path.split(curfile)[1]
    retstring = ":".join((
        folder,
        str(currentIndex()['batch']),
        str(currentIndex()['session']),
        str(itemsRemain())))
    return retstring


@app.route('/info/reset')
def resetSession():
    resetSession(0)
    return "OK", 200

if __name__ == '__main__':
    for each in cfgDB['actions'].itervalues():
        if not os.path.exists(each):
            os.makedirs(each)
    app.run(host='0.0.0.0', debug=True)
