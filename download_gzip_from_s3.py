import boto3
import gzip
from io import BytesIO
import shutil

aws_session = boto3.Session(aws_access_key_id='',  ### AWS ACCESS KEY HERE
                            aws_secret_access_key='')  ### AWS SECRET KEY HERE

s3_client = aws_session.client('s3')


def download_gzip_from_s3(bucket, key):
    input_file_buffer = BytesIO()
    output_file_buffer = BytesIO()

    s3_client.download_fileobj(Bucket=bucket,
                               Key=key,
                               Fileobj=input_file_buffer)

    input_file_buffer.seek(0)
    with gzip.GzipFile(fileobj=input_file_buffer, mode='rb') as gz:
        shutil.copyfileobj(gz, output_file_buffer)

    return output_file_buffer.getvalue()
