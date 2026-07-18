import argparse
import os

import boto3

IGNORE = {".venv", ".git", "__pycache__", "node_modules"}
IGNORE_FILES = {".env", ".DS_Store"}

# Create the S3 client ONCE (reused for every upload).
# Credentials come from the env vars (source .env first!).
s3 = boto3.client(
    "s3",
    endpoint_url=os.environ["MGC_ENDPOINT"],
    aws_access_key_id=os.environ["MGC_ACCESS_KEY"],
    aws_secret_access_key=os.environ["MGC_SECRET_KEY"],
)


def push(source, bucket):
    """Upload every file inside `source` to the bucket."""
    count = 0
    for root, folders, files in os.walk(source):
        # prune ignored folders so os.walk never enters them
        folders[:] = [f for f in folders if f not in IGNORE]

        for name in files:
            # skip sensitive/junk files
            if name in IGNORE_FILES:
                continue

            local_path = os.path.join(root, name)
            key = os.path.relpath(local_path, source)

            s3.upload_file(local_path, bucket, key)
            print(f"uploaded: {key}")
            count += 1

    print(f"\ndone! {count} files uploaded.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="magalu-backup",
        description="Incremental backup CLI for S3-compatible storage",
    )
    parser.add_argument("command", choices=["push"])
    parser.add_argument("folder")
    parser.add_argument("--bucket", default="grazi-backup-test")

    args = parser.parse_args()

    if args.command == "push":
        push(args.folder, args.bucket)
