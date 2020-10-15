import os
import sys
import boto3
local_directory = 'datasets/'
bucket = 'computacao-nuvem'
destination = 'datasets/'

def upload_dir_s3(local_dir='datasets/',bucket='computacao-nuvem',destination='datasets/'):
    client = boto3.client('s3')
    # enumerate local files recursively
    for root, dirs, files in os.walk(local_dir):

        for filename in files:

            # construct the full local path
            local_path = os.path.join(root, filename)

            # construct the full Dropbox path
            relative_path = os.path.relpath(local_path, local_dir)
            s3_path = os.path.join(destination, relative_path)

            # relative_path = os.path.relpath(os.path.join(root, filename))
            try:
                client.head_object(Bucket=bucket, Key=s3_path)

                # try:
                    # client.delete_object(Bucket=bucket, Key=s3_path)
                # except:
                    # print "Unable to delete %s..." % s3_path
            except:
                client.upload_file(local_path, bucket, s3_path)

#upload_dir_s3()