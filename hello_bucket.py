import os
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ["MGC_ENDPOINT"],
    aws_access_key_id=os.environ["MGC_ACCESS_KEY"],
    aws_secret_access_key=os.environ["MGC_SECRET_KEY"],
)

# lista buckets
print(s3.list_buckets())

# sobe um arquivo de teste
s3.put_object(Bucket="grazi-backup-test", Key="hello.txt", Body=b"hello magalu!")
print(s3.list_objects_v2(Bucket="grazi-backup-test"))
