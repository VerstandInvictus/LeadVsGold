import os
import shutil
import pymongo
from datetime import timedelta
from flask import Flask, send_file, make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods
        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)


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
    files = os.listdir(cfgDB['outputFolder'])
    print files
    return len(files)


@app.route('/image/<nonce>')
@crossdomain(origin='*')
def showFile(nonce):
    return send_file(getCurFile()["location"])


@app.route('/next/<action>/<nonce>')
@crossdomain(origin='*')
def skipForward(action, nonce):
    curFile = getCurFile()
    if curFile == cfgDB['noneObject']:
        setIndex(0)
        return send_file(cfgDB['noneObject']["location"])
    newPath = os.path.join(cfgDB['actions'][action], curFile["name"])
    if curFile['location'] != newPath:
        shutil.copy2(curFile['location'], newPath)
        os.remove(curFile['location'])
        updateLocation(currentIndex()['batch'], newPath)
    incrementIndex(1)
    return send_file(getCurFile()['location'])


@app.route('/imgtap')
@crossdomain(origin='*')
def tapAction():
    curFile = getCurFile()
    newPath = os.path.join(cfgDB['actions']['tap'], curFile['name'])
    shutil.copy2(curFile['location'], newPath)
    return "OK", 200


@app.route('/prev/<nonce>')
@crossdomain(origin='*')
def skipBack(nonce):
    incrementIndex(-1)
    return send_file(getCurFile()['location'])


@app.route('/info/<nonce>')
@crossdomain(origin="*")
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
@crossdomain(origin="*")
def resetSession():
    resetSession(0)
    return "OK", 200

if __name__ == '__main__':
    for each in cfgDB['actions'].itervalues():
        if not os.path.exists(each):
            os.makedirs(each)
    app.run(host='0.0.0.0', debug=True)
