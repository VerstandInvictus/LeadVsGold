import os
import shutil
import config
from flask import Flask, send_file

app = Flask(__name__)

stackFolder = os.path.join(os.getcwdu(), config.inputfolder)
outputFolder = os.path.join(os.getcwdu(), "output")
stackFiles = os.listdir(stackFolder)

actions = dict(
    up=os.path.join(outputFolder, config.upfolder),
    down=os.path.join(outputFolder, config.downfolder),
    skip=os.path.join(outputFolder, "skipped"),
)


def getAFile():
    global stackFiles
    cf = stackFiles.pop(0)
    cfp = os.path.join(stackFolder, cf)
    return dict(
        filename=cf,
        obj=cfp
    )


def listFiles():
    return str(stackFiles)


@app.route('/image')
def showFile():
    return send_file(curFile['obj'])


@app.route('/next/<action>')
def skipForward(action):
    global curFile
    shutil.copy2(
        curFile['obj'], os.path.join(actions[action], curFile['filename']))
    os.remove(curFile['obj'])
    curFile = getAFile()
    return "OK", 200


if __name__ == '__main__':
    for each in actions:
        if not os.path.exists(each):
            os.makedirs(each)
    curFile = getAFile()
    app.run(debug=True)
