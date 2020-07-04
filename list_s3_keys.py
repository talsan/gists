import boto3
import re

aws_session = boto3.Session(aws_access_key_id='',  ### AWS ACCESS KEY HERE
                            aws_secret_access_key='')  ### AWS SECRET KEY HERE

s3_client = aws_session.client('s3')


def list_keys(bucket, prefix='', suffix='', full_path=True, remove_ext=False):
    # get pages for bucket and prefix
    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

    # iterate through pages and store the keys in a list
    keys = []
    for page in page_iterator:
        if 'Contents' in page.keys():
            for content in page['Contents']:
                key = content['Key']
                if not key.endswith('/'):  # ignore directories
                    if key.endswith(suffix):
                        if not full_path:  # remove prefix if full_path == False
                            key = re.sub(prefix, '', key)
                        if remove_ext:  # remove extension (anything after last ".") if remove_ext == True
                            key = re.sub('\.[^.]+$', '', key)
                        keys.append(key)
    return keys
