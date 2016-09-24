import os
import re
import arrow
import boto3
import config
import time


def checkTableExists(client, checkname):
    try:
        check = client.describe_table(
            TableName=checkname
        )
        res = check['Table']['TableStatus']
        print "currently {0}: {1}".format(res, checkname)
        return res
    except:
        return False


def createTable(client, cname):
    table = client.create_table(
        TableName=cname,
        KeySchema=[
            {
                'AttributeName': '_id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': '_id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    )
    print "created {0}".format(cname)
    return table


def clearTable(client, tname):
    if checkTableExists(client, tname):
        client.delete_table(TableName=tname)
        print "deleted {0}".format(tname)
        time.sleep(5)
        createTable(client, tname)
        time.sleep(5)
    res = checkTableExists(client, tname)
    while True:
        if res == 'ACTIVE':
            return
        else:
            time.sleep(1)
            res = checkTableExists(client, tname)


dbclient = boto3.client(
    'dynamodb',
    aws_access_key_id=config.awskeyid,
    aws_secret_access_key=config.awskey,
    region_name='us-west-2'
)
initdbn = config.dbname + '-init'
fldbn = config.dbname + '-fldb'

clearTable(dbclient, initdbn)
dbresource = boto3.resource(
    'dynamodb',
    aws_access_key_id=config.awskeyid,
    aws_secret_access_key=config.awskey,
    region_name='us-west-2'
)
initdb = dbresource.Table(initdbn)
print "reset init DB\n"
clearTable(dbclient, fldbn)
fldb = dbresource.Table(fldbn)
print "reset filelist DB\n"


outf = os.path.join(os.getcwdu(), "output")
inf = os.path.join(os.getcwdu(), config.inputfolder)
stackFiles = list()
fileList = [x for x in os.listdir(inf) if not os.path.isdir(x)]
fileList.sort(key=lambda x: os.path.getmtime(os.path.join(inf, x)))
fileList.reverse()
print "{0} files processed into DB.".format(len(fileList))
for f in fileList:
    if os.path.splitext(f)[1] in (
            ".jpg", ".jpeg", ".gif", ".png"):
        stackFiles.append(f)
count = 1
stackQueue = list()
for f in stackFiles:
    try:
        creator = re.search('__(.+?)__', f).group(1)
        creator = re.sub(',', ' /', creator)
    except AttributeError:
        creator = "No Creator"
    mtime = arrow.get(
        os.path.getmtime(
            os.path.join(inf, f))).to('US/Pacific').format("M/D/YYYY")
    fileobj = dict(
        _id=count,
        name=f,
        location=os.path.join(inf, f),
        creator=creator,
        mtime=mtime)
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
for folder in initDict['actions'].itervalues():
    if not os.path.exists(folder):
        os.makedirs(folder)
for each in initDict['actions'].itervalues():
    if not os.path.exists(each):
        os.makedirs(each)
initdb.put_item(Item=initDict)
with fldb.batch_writer() as fldbatch:
    for each in stackQueue:
        fldbatch.put_item(Item=each)
initdb.put_item(Item=indexes)
