import argparse
import os

import boto3

IGNORE = {".venv", ".git", "__pycache__", "node_modules"}
IGNORE_FILES = {".env", ".DS_Store"}

_s3 = None


def get_s3():
    global _s3
    if _s3 is None:
        _s3 = boto3.client(
            "s3",
            endpoint_url=os.environ["MGC_ENDPOINT"],
            aws_access_key_id=os.environ["MGC_ACCESS_KEY"],
            aws_secret_access_key=os.environ["MGC_SECRET_KEY"],
        )
    return _s3


def push(source, bucket):
    """Upload every file inside `source` to the bucket."""
    s3 = get_s3()
    count = 0
    for root, folders, files in os.walk(source):
        folders[:] = [f for f in folders if f not in IGNORE]

        for name in files:
            if name in IGNORE_FILES:
                continue

            local_path = os.path.join(root, name)
            key = os.path.relpath(local_path, source)

            s3.upload_file(local_path, bucket, key)
            print(f"uploaded: {key}")
            count += 1

    print(f"\ndone! {count} files uploaded.")


def main():
    parser = argparse.ArgumentParser(
        prog="backup",
        description="Incremental backup CLI for S3-compatible storage",
    )
    parser.add_argument("command", choices=["push"])
    parser.add_argument("folder")
    parser.add_argument("--bucket", default="grazi-backup-test")

    args = parser.parse_args()

    if args.command == "push":
        push(args.folder, args.bucket)


if __name__ == "__main__":
    main()
