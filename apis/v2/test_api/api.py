from apis.v1.test_api.api import TestApi


class TestApiV2(TestApi):
    def __init__(self, request, request_args):
        super().__init__(request, request_args)
        self.version = '2'
        
    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        super().populate_request_arguments()
        self.degree = self.request_args.get('degree')

    def prepare_response(self):
        super().prepare_response()
        self.response['data']['degree'] = self.degree
