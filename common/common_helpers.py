import errno
import logging
import os
import random
import types


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
