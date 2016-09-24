import os
import boto3
import config

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

folderdb = dbresource.table('lvgfolders')


def listFolders():
    basedir = os.path.join('webapp', 'folders')
    dirlist = [d for d in os.listdir(basedir) if os.path.isdir(os.path.join(
        basedir, d))]
    return dirlist


def foldersToDb(dirlist):
    folderdb.put_item(
        Item={
            "index": 1,
            "folders": dirlist
        }
    )

if __name__ == "__main__":
    folderdb.delete_item(
        Key={"index": 1}
    )
    dlist = listFolders()
    foldersToDb(dlist)
