import os
import shutil
import boto3
from flask import Flask, send_file, request, Response, json
from flask_cors import CORS
import config

app = Flask(__name__)
CORS(app)

dbclient = boto3.client(
    'dynamodb',
    aws_access_key_id=config.awskeyid,
    aws_secret_access_key=config.awskey,
    region_name='us-west-2'
)
dbresource = boto3.resource(
    'dynamodb',
    aws_access_key_id=config.awskeyid,
    aws_secret_access_key=config.awskey,
    region_name='us-west-2'
)
folderdb = dbresource.Table('lvgfolders')


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
    initdbn = dbname + '-init'
    fldbn = dbname + '-fldb'
    if whichdb == "fldb":
        return dbresource.Table(fldbn)
    if whichdb == "initdb":
        return dbresource.Table(initdbn)
    if whichdb == "cfgdb":
        return dbresource.Table(initdbn).get_item(
            Key={'_id': "initDict"}
        )['Item']


def currentIndex(dbname):
    return dbHandles(dbname, 'initdb').get_item(
        Key={"_id": "index"}
    )['Item']


def updateLocation(index, location, dbname):
    dbHandles(dbname, 'fldb').update_item(
        Key={"_id": index},
        UpdateExpression="SET loc = :l",
        ExpressionAttributeValues={
            ":l": location
        }
    )


def getCurFile(dbname):
    curFile = dbHandles(dbname, 'fldb').get_item(
        Key={"_id": currentIndex(dbname)["bat"]})['Item']
    if curFile is None:
        return dbHandles(dbname, 'cfgdb')["noneObject"]
    else:
        return curFile


def incrementIndex(num, dbname):
    dbHandles(dbname, 'initdb').update_item(
        Key={'_id': "index"},
        UpdateExpression="SET bat = :b, ses = :s",
        ExpressionAttributeValues={
            ":b": currentIndex(dbname)["bat"] + num,
            ":s": currentIndex(dbname)["ses"] + num
        }
    )


def setIndex(num, dbname):
    dbHandles(dbname, 'initdb').update_item(
        Key={'_id': "index"},
        UpdateExpression="SET bat = :b",
        ExpressionAttributeValues={
            ":b": num,
        }
    )


def resetSession(num, dbname):
    dbHandles(dbname, 'initdb').update_item(
        Key={'_id': "index"},
        UpdateExpression="SET ses = :s",
        ExpressionAttributeValues={
            ":s": num
        }
    )


def itemsRemain(dbname):
    files = os.listdir(dbHandles(dbname, 'cfgdb')['stackFolder'])
    return len(files)


@app.route('/folders')
def getFolders():
    return jsonWrapper(folderdb.get_item(
        Key={"index": 1}
    )['Item']['folders'], isCursor=0)


@app.route('/<dbname>/image/<nonce>')
def showFile(nonce, dbname):
    return send_file(getCurFile(dbname)["loc"])


@app.route('/<dbname>/next/<action>/<nonce>')
def skipForward(action, nonce, dbname):
    curFile = getCurFile(dbname)
    if curFile == dbHandles(dbname, 'cfgdb')['noneObject']:
        setIndex(0, dbname)
        return send_file(dbHandles(dbname, 'cfgdb')['noneObject']["loc"])
    newPath = os.path.join(dbHandles(
        dbname, 'cfgdb')['actions'][action], curFile["name"])
    if curFile['loc'] != newPath:
        shutil.copy2(curFile['loc'], newPath)
        os.remove(curFile['loc'])
        updateLocation(currentIndex(dbname)['bat'], newPath, dbname)
    incrementIndex(1, dbname)
    return send_file(getCurFile(dbname)['loc'])


@app.route('/<dbname>/imgtap')
def tapAction(dbname):
    curFile = getCurFile(dbname)
    newPath = os.path.join(dbHandles(
        dbname, 'cfgdb')['actions']['tap'], curFile['name'])
    shutil.copy2(curFile['loc'], newPath)
    return "OK", 200


@app.route('/<dbname>/prev/<nonce>')
def skipBack(nonce, dbname):
    incrementIndex(-1, dbname)
    return send_file(getCurFile(dbname)['loc'])


@app.route('/<dbname>/info/<nonce>')
def sendFolder(nonce, dbname):
    f = getCurFile(dbname)
    npath = f['loc']
    curfile = os.path.split(npath)[0]
    folder = os.path.split(curfile)[1]
    creator = f['creator']
    mtime = f['mtime']
    retstring = ":".join((
        folder,
        creator,
        str(currentIndex(dbname)['bat']),
        str(currentIndex(dbname)['ses']),
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
