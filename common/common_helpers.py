import errno
import io
import logging
import os
import random
import types

from PIL import Image
import boto3

from app import get_settings
from common.constants import PROFILE_IMAGE_DIMENSIONS


class CommonHelpers(object):
    @staticmethod
    def generate_six_digit_random_code():
        """
        Generates 6 digit random code
        """
        code = random.randrange(100000, 999999, 1)
        return code

    @staticmethod
    def get_logger(log_file_path, log_file):
        """
        Gets logger file

        :param str log_file_path: log file path
        :param log_file: log file

        :returns log file
        """
        logger = logging.getLogger()
        if not os.path.isdir(log_file_path):
            os.makedirs(log_file_path)
        file_logging_formatter = logging.Formatter('%(asctime)s %(name)s %(message)s')
        file_handler = logging.FileHandler(filename='{log_file_path}/{log_file}'.format(
            log_file_path=log_file_path, log_file=log_file
        ))
        file_handler.suffix = '%Y-%m-%d'
        file_handler.setFormatter(file_logging_formatter)
        file_handler.setLevel(logging.INFO)
        file_handler.suffix = '%Y-%m-%d'
        logger.addHandler(file_handler)
        return logger

    @staticmethod
    def get_settings_data_from_environment_variable(env_name='APPLICATION_SETTINGS'):
        """
        Gets settings data from environment variable

        :param str env_name: environment variable name

        :rtype dict
        :returns settings data
        """
        settings_path = os.getenv(env_name)
        settings_module = CommonHelpers.from_pyfile(settings_path)
        settings_data = {}
        for setting in dir(settings_module):
            if setting.isupper():
                settings_data[setting] = getattr(settings_module, setting)
        return settings_data

    @staticmethod
    def from_pyfile(filename, silent=False):
        """Updates the values in the config from a Python file.  This function
        behaves as if the file was imported as module with the
        :meth:`from_object` function.

        :param filename: the filename of the config.  This can either be an
                         absolute filename or a filename relative to the
                         root path.
        :param silent: set to ``True`` if you want silent failure for missing
                       files.

        .. versionadded:: 0.7
           `silent` parameter.
        """
        d = types.ModuleType("config")
        d.__file__ = filename
        try:
            with open(filename, mode="rb") as config_file:
                exec(compile(config_file.read(), filename, "exec"), d.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR, errno.ENOTDIR):
                return False
            e.strerror = "Unable to load configuration file (%s)" % e.strerror
            raise
        return d

    @staticmethod
    def process_image(image, is_profile_image=False, is_post_image=False):
        """
        Process image. Verifies the size of image and converts image to required size and also makes small image
        if required

        :param FileStorage image: image
        :param boolean is_profile_image: profile image flag
        :param boolean is_post_image: post image flag

        :returns image
        """
        uploaded_image = Image.open(image)
        image_dimensions = uploaded_image.size
        if is_profile_image:
            image = uploaded_image
            if image_dimensions != PROFILE_IMAGE_DIMENSIONS:
                image = uploaded_image.resize(PROFILE_IMAGE_DIMENSIONS)
        elif is_post_image:
            image = uploaded_image
        image = CommonHelpers.convert_image_to_bytes(image=image, format=uploaded_image.format.lower())
        return image

    @staticmethod
    def put_s3_object(file, file_name, file_path=None):
        """
        Puts storage object into s3

        :param file: file
        :param str file_name: file name
        :param str file_path: file path

        :rtype bool
        :returns file uploading flag
        """
        settings = get_settings()
        try:
            is_object_uploaded = True
            file_key = file_name
            bucket = settings.aws_s3_bucket_name
            client = boto3.client(
                's3', aws_secret_access_key=settings.aws_secret_access_key, aws_access_key_id=settings.aws_access_key_id
            )
            if file_path:
                file_key = '{directory}/{file_name}'.format(directory=file_path, file_name=file_name)
            client.put_object(
                Bucket=bucket, Key=file_key, Body=file, ACL=settings.aws_acl_public_read,
                StorageClass=settings.aws_standard_storage_class
            )
        except Exception:
            logger = CommonHelpers.get_logger(log_file_path='logs/aws', log_file='s3_logs.log')
            logger.exception('Exception occurred while uploading storage object on AWS S3')
            is_object_uploaded = False
        return is_object_uploaded

    @staticmethod
    def convert_image_to_bytes(image, format):
        """
        Converts image file into bytes. It also converts format of image to png

        :param image: image
        :param str format: image format

        :returns bytes image
        """
        in_mem_file = io.BytesIO()
        image.save(in_mem_file, format=format)
        return in_mem_file.getvalue()
