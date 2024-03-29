import json

import boto3
from passlib.context import CryptContext
from jose import jwt

from app import get_settings
from common.constants import SUCCESS_STATUS_CODES
from security.aes import AESCipher

settings = get_settings()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


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


def get_password_hash(password):
    """
    Gets password hash

    :param str password: password

    :rtype str
    :returns password hash
    """
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(plain_password, hashed_password):
    """
    Verifies password

    :param str plain_password: plain password
    :param str hashed_password: hashed password

    :rtype bool
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(data: dict):
    """
    Creates JWT Token
    """
    encoded_jwt_token = jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt_token


def encrypt_response(request_args, response):
    """
    Encrypt response

    :param request_args: request args
    :param response: response

    :rtype str
    :returns encrypted response
    """
    request_args = json.loads(request_args.json())
    if (
            response.get('status_code') in SUCCESS_STATUS_CODES and
            request_args.get('encryption_disable_key') != settings.encryption_disable_key
    ):
        return AESCipher.encrypt(response)
    return response
