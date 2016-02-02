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


class fileList(object):

    def __init__(self):
        self.stackFolder = os.path.join(os.getcwdu(), config.inputfolder)
        self.outputFolder = os.path.join(os.getcwdu(), "output")
        self.stackFiles = os.listdir(self.stackFolder)
        self.actions = dict(
            up=os.path.join(self.outputFolder, config.upfolder),
            down=os.path.join(self.outputFolder, config.downfolder),
            skip=os.path.join(self.outputFolder, "skipped"),
        )
        self.history = list()
        self.curFile = None
        self.getAFile()

    def getAFile(self):
        try:
            cf = self.stackFiles.pop()
            cfp = os.path.join(self.stackFolder, cf)
        except IndexError:
            self.reInit()
            return None
        self.curFile = dict(
            filename=cf,
            obj=cfp
        )

    def getOldFile(self):
        if len(self.history) != 0:
            hf = self.history.pop()
            cf = hf['filename']
            cfp = hf['obj']
            dst = os.path.join(self.stackFolder, cf)
            shutil.copy(cfp, dst)
            self.stackFiles.append(cf)
        else:
            self.curFile = None

    def reInit(self):
        self.stackFiles = os.listdir(self.stackFolder)
        if len(self.stackFiles) == 0:
            pass
        else:
            self.getAFile()


@app.route('/image/<nonce>')
@crossdomain(origin='*')
def showFile(nonce):
    print fl.history
    if fl.curFile is not None:
        try:
            return send_file(fl.curFile['obj'])
        except IOError:
            fl.reInit()
            return send_file('webapp\\img\\nomore.png')
    else:
        fl.reInit()
        return send_file('webapp\\img\\nomore.png')


@app.route('/next/<action>')
@crossdomain(origin='*')
def skipForward(action):
    cf = fl.curFile
    if cf is not None:
        wf = os.path.join(fl.stackFolder, cf['obj'])
        np = os.path.join(fl.actions[action], cf['filename'])
        print fl.actions[action]
        print cf['filename']
        print np
        shutil.copy2(wf, np)
        os.remove(wf)
        check = fl.history[-1] if len(fl.history) > 0 else None
        if check is None:
            fl.history.append(dict(
                filename=cf['filename'],
                obj=np
                ))
        else:
            if cf['filename'] != check['filename']:
                print "adnew"
                fl.history.append(dict(
                    filename=cf['filename'],
                    obj=np
                ))
        fl.getAFile()
    else:
        pass
    return "OK", 200


@app.route('/prev')
@crossdomain(origin='*')
def skipBack():
    fl.getOldFile()
    cf = fl.curFile
    if cf is not None:
        wf = os.path.join(fl.stackFolder, cf['obj'])
        check = fl.history[-1] if len(fl.history) > 0 else None
        if check is None:
            fl.history.append(dict(
                filename=cf['filename'],
                obj=wf
            ))
        else:
            if cf != check:
                print "adnew"
                fl.history.append(dict(
                    filename=cf['filename'],
                    obj=wf
                ))
    return "OK", 200


if __name__ == '__main__':
    fl = fileList()
    for each in fl.actions.itervalues():
        if not os.path.exists(each):
            os.makedirs(each)
    app.run(debug=True)
