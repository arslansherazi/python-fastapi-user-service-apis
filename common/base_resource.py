import json

from requests import codes

from common.common_helpers import CommonHelpers
from common.constants import SUCCESS_STATUS_CODES


class BaseResource(object):
    def __init__(self, request, request_args):
        self.request = request
        self.status_code = 200
        self.version = ''
        self.end_point = ''
        self.request_args = json.loads(request_args.json())
        self.response = {}
        self.is_send_response = False

    def request_flow(self):
        logger = None
        try:
            log_file_path = 'logs/apis/{end_point}'.format(end_point=self.end_point)
            log_file = '{end_point}_v{version}.log'.format(end_point=self.end_point, version=self.version)
            logger = CommonHelpers.get_logger(log_file_path, log_file)
            self.process_request()
            return self.send_response()
        except Exception:
            if logger:
                logger.exception()
            self.status_code = codes.INTERNAL_SERVER_ERROR
            self.response = {
                'message': 'Internal Server Error'
            }
            return self.send_response()

    def process_request(self):
        pass

    def populate_request_arguments(self):
        pass

    def initialize_class_attributes(self):
        pass

    def send_response(self):
        self.response['success'] = True
        if self.status_code not in SUCCESS_STATUS_CODES:
            self.response['success'] = False
        self.response['status_code'] = self.status_code
        self.response['cmd'] = self.request.url.path
        return self.response

