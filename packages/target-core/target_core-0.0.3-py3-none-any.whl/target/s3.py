#!/usr/bin/env python3
import os
import backoff
import boto3
from typing import Callable, Dict, Any
from botocore.exceptions import ClientError

from target.logger import get_logger
LOGGER = get_logger()


def retry_pattern() -> Callable:
    return backoff.on_exception(
        backoff.expo,
        ClientError,
        max_tries=5,
        on_backoff=log_backoff_attempt,
        factor=10)


def log_backoff_attempt(details: Dict) -> None:
    LOGGER.info("Error detected communicating with Amazon, triggering backoff: %d try", details.get("tries"))


@retry_pattern()
def create_client(config: Dict) -> Any:
    LOGGER.info("Attempting to create AWS session")

    # Get the required parameters from config file and/or environment variables
    aws_access_key_id = config.get('aws_access_key_id') or os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = config.get('aws_secret_access_key') or os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_session_token = config.get('aws_session_token') or os.environ.get('AWS_SESSION_TOKEN')
    aws_profile = config.get('aws_profile') or os.environ.get('AWS_PROFILE')
    aws_endpoint_url = config.get('aws_endpoint_url')

    # AWS credentials based authentication
    if aws_access_key_id and aws_secret_access_key:
        aws_session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token)
    # AWS Profile based authentication
    else:
        aws_session = boto3.session.Session(profile_name=aws_profile)

    if aws_endpoint_url:
        return aws_session.client('s3', endpoint_url=aws_endpoint_url)
    else:
        return aws_session.client('s3')


@retry_pattern()
def upload_file(s3_client: Any, file_metadata: Dict, config: Dict[str, Any]) -> None:

    if config.get('encryption_type', 'none').lower() == "none":
        # No encryption config (defaults to settings on the bucket):
        encryption_desc = ''
        encryption_args = None
    elif config.get('encryption_type', 'none').lower() == 'kms':
        if config.get('encryption_key'):
            encryption_desc = " using KMS encryption key ID '{}'".format(config.get('encryption_key'))
            encryption_args = {'ServerSideEncryption': 'aws:kms', 'SSEKMSKeyId': config.get('encryption_key')}
        else:
            encryption_desc = ' using default KMS encryption'
            encryption_args = {'ServerSideEncryption': 'aws:kms'}
    else:
        raise NotImplementedError(
            "Encryption type '{}' is not supported. "
            "Expected: 'none' or 'KMS'"
            .format(config.get('encryption_type')))

    LOGGER.info(
        "Uploading {} to bucket {} at {}{}".format(
            str(file_metadata['absolute_path']),
            config.get('s3_bucket'),
            file_metadata['relative_path'],
            encryption_desc))

    s3_client.upload_file(
        str(file_metadata['absolute_path']),
        config.get('s3_bucket'),
        file_metadata['relative_path'],
        ExtraArgs=encryption_args)


def upload_files(file_data: Dict, config: Dict[str, Any]) -> None:
    if not config.get('local', False):
        s3_client = create_client(config)
        for stream, file_metadata in file_data.items():
            if file_metadata['absolute_path'].exists():
                upload_file(
                    s3_client,
                    file_metadata,
                    config)
                LOGGER.debug("{} file {} uploaded to {}".format(stream, file_metadata['relative_path'], config.get('s3_bucket')))

                # NOTE: Remove the local file(s)
                file_metadata['absolute_path'].unlink()
