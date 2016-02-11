import os
import config
import pymongo

client = pymongo.MongoClient()
db = client.leadvsgold
initdb = db.init
fl = db.fileList
outf = os.path.join(os.getcwdu(), "webapp", "output")
inf = os.path.join(os.getcwdu(), "webapp", config.inputfolder)
stackFiles = list()
for f in os.listdir(inf):
    if os.path.splitext(f)[1] in (
            ".jpg", ".jpeg", ".gif", ".png"):
        stackFiles.append(f)
count = 1
stackQueue = list()
for f in stackFiles:
    fileobj = dict(
        _id=count,
        name=f,
        location=os.path.join(inf, f))
    stackQueue.append(fileobj)
    count += 1
initDict = dict(
    _id="initDict",
    stackFolder=inf,
    outputFolder=outf,
    actions=dict(
        up=os.path.join(outf, config.upfolder),
        down=os.path.join(outf, config.downfolder),
        skip=os.path.join(outf, "skipped"),
        tap=os.path.join(outf, config.tapfolder)),
    noneObject=dict(
        name='nomore.png',
        location='webapp\\img\\nomore.png'))
indexes = dict(
    _id="index",
    batch=1,
    session=1,)
fl.drop()
initdb.drop()
initdb.insert_one(initDict)
fl.insert_many(stackQueue)
initdb.insert_one(indexes)
