import boto3
import gzip
from io import BytesIO
import shutil

aws_session = boto3.Session(aws_access_key_id='',  ### AWS ACCESS KEY HERE
                            aws_secret_access_key='')  ### AWS SECRET KEY HERE

s3_client = aws_session.client('s3')


def upload_gzip_to_s3(bucket, key, content, content_type=None):
    input_file_buffer = BytesIO(content)
    compressed_file_buffer = BytesIO()
    with gzip.GzipFile(fileobj=compressed_file_buffer, mode='wb') as gz:
        shutil.copyfileobj(input_file_buffer, gz)
    compressed_file_buffer.seek(0)

    extra_args = {'ContentEncoding': 'gzip'}
    if content_type is not None:
        extra_args.update({'ContentType': content_type})

    response = s3_client.upload_fileobj(Bucket=bucket, Key=key, Fileobj=compressed_file_buffer, ExtraArgs=extra_args)
    return response
