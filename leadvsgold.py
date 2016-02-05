import os
import shutil
import config
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


class fileObject(object):
    def __init__(self, name, location):
        self.name=name
        self.location=location


class fileList(object):

    def __init__(self):
        self.stackFolder = os.path.join(os.getcwdu(), config.inputfolder)
        self.outputFolder = os.path.join(os.getcwdu(), "output")
        self.stackFiles = os.listdir(self.stackFolder)
        self.actions = dict(
            up=os.path.join(self.outputFolder, config.upfolder),
            down=os.path.join(self.outputFolder, config.downfolder),
            skip=os.path.join(self.outputFolder, "skipped"),
            tap=os.path.join(self.outputFolder, config.tapfolder)
        )
        self.stackQueue = list()
        self.noneObject = fileObject('nomore.png', 'webapp\\img\\nomore.png')
        for f in self.stackFiles:
            fileobj = fileObject(f, os.path.join(
                self.stackFolder, f))
            self.stackQueue.append(fileobj)
        self.index = 0

    def updateLocation(self, index, location):
        self.stackQueue[index].location = location

    def getCurFile(self):
        try:
            return self.stackQueue[self.index]
        except IndexError:
            return self.noneObject

    def incrementIndex(self, num):
        self.index += num

    def setIndex(self, num):
        self.index = num


@app.route('/image/<nonce>')
@crossdomain(origin='*')
def showFile(nonce):
    return send_file(fl.getCurFile().location)


@app.route('/next/<action>/<nonce>')
@crossdomain(origin='*')
def skipForward(action, nonce):
    curFile = fl.getCurFile()
    if curFile == fl.noneObject:
        fl.setIndex(0)
        return send_file(fl.noneObject.location)
    newPath = os.path.join(fl.actions[action], curFile.name)
    if curFile.location != newPath:
        shutil.copy2(curFile.location, newPath)
        os.remove(curFile.location)
        fl.updateLocation(fl.index, newPath)
    fl.incrementIndex(1)
    return send_file(fl.getCurFile().location)


@app.route('/imgtap')
@crossdomain(origin='*')
def tapAction():
    curFile = fl.getCurFile()
    newPath = os.path.join(fl.actions['tap'], curFile.name)
    shutil.copy2(curFile.location, newPath)
    return "OK", 200


@app.route('/prev/<nonce>')
@crossdomain(origin='*')
def skipBack(nonce):
    fl.incrementIndex(-1)
    return send_file(fl.getCurFile().location)


@app.route('/index/<nonce>')
@crossdomain(origin='*')
def sendIndex(nonce):
    return fl.index


@app.route('/folder/<nonce>')
@crossdomain(origin="*")
def sendFolder(nonce):
    path = fl.getCurFile().location()
    curfile = os.path.split(path)[0]
    folder = os.path.split(curfile)[1]
    return folder


if __name__ == '__main__':
    fl = fileList()
    for each in fl.actions.itervalues():
        if not os.path.exists(each):
            os.makedirs(each)
    app.run(host='0.0.0.0', debug=True)
