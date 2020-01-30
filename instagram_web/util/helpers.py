import boto3, botocore
from config import Config
import os
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("S3_KEY"),
    aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY")
)

def upload_file_to_s3(file, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            os.getenv("S3_BUCKET_NAME"),
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something happened: ", e)
        return e

    # return "{}{}".format(Config["S3_LOCATION"], file.filename)
    return file.filename