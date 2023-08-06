import os
import json

region = os.environ.get("aws_region")
userpool = os.environ.get("aws_userpool_id")
app_client_id = os.environ.get("aws_app_client_id")
document_bucket_name = os.environ.get("aws_document_bucket_name")
key = os.environ.get("aws_key")
secret = os.environ.get("aws_secret_key")
env = {
        "region"    : region,
        "userpool_id" : userpool,
        "app_client_id" : app_client_id,
        "document_bucket_name": document_bucket_name,
        "key": key,
        "secret": secret
    }