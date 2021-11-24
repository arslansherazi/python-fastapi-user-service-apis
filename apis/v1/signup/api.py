from common.base_resource import BaseResource


class Signup(BaseResource):
    def __init__(self, request, request_args):
        super().__init__(request, request_args)
        self.version = '1'
        self.end_point = 'signup'

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.username = self.request_args.get('username')
        self.email = self.request_args.get('email')
        self.password = self.request_args.get('password')
        self.name = self.request_args.get('name')
        self.profile_image = self.request_args.get('profile_image')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        pass

    def verify_username(self):
        """
        Verifies username
        """
        is_username_available = None