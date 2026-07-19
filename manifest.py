import json

# Key fixa onde o manifest vive dentro do bucket.
MANIFEST_KEY = ".backup/manifest.json"


def load_manifest(s3, bucket):
    """Baixa o manifest do bucket e devolve como dict.

    Se o objeto ainda nao existe (primeiro push), devolve {} vazio.
    """
    try:
        # Busca o objeto no bucket pela Key
        response = s3.get_object(Bucket=bucket, Key=MANIFEST_KEY)

       # Desserializa
        return json.loads(response["Body"].read())

    except s3.exceptions.NoSuchKey:
        return {}


def save_manifest(s3, bucket, manifest):
    """Serializa o manifest (dict) e grava como objeto JSON no bucket."""

    body = json.dumps(manifest, indent=2)

    s3.put_object(Bucket=bucket, Key=MANIFEST_KEY, Body=body)
