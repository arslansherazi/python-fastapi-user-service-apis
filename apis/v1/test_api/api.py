from common.base_resource import BaseResource


class TestApi(BaseResource):
    def __init__(self, request, request_args):
        super().__init__(request, request_args)
        self.version = '1'
        self.end_point = 'test_api'

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.name = self.request_args.get('name')
        self.roll_no = self.request_args.get('roll_no')

    def prepare_response(self):
        self.response = {
            'success': True,
            'data': {
                'name': self.name,
                'roll_no': self.roll_no
            }
        }

    def process_request(self):
        self.populate_request_arguments()
        self.prepare_response()
