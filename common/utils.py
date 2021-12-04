import boto3

from app import get_settings

settings = get_settings()


def get_boto_client(service):
    """
    Gets boto client

    :param str service: AWS service

    :return  boto client
    """
    boto_client = boto3.client(
        service, aws_secret_access_key=settings.aws_secret_access_key,
        aws_access_key_id=settings.aws_access_key_id, region_name=settings.aws_ses_region
    )
    return boto_client
