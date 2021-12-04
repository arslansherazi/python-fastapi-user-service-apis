from app import get_settings
from common.base_resource import BaseResource
from common.utils import verify_password, create_jwt_token
from models.v1.user import User
from repositories.v1.user_repo import UserRepository
from security.aes import AESCipher


class Login(BaseResource):
    def __init__(self, request, request_args):
        super().__init__(request, request_args)
        self.version = '1'
        self.end_point = 'login'
        self.settings = get_settings()
        self.user_login_info = None

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.user_type = self.request_args.get('user_type')
        self.username = self.request_args.get('username')
        self.password = self.request_args.get('password')

    def verify_user(self):
        """
        Verifies user exist in system
        """
        self.user_login_info = User.get_login_info(self.username)
        if not self.user_login_info:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'success': False,
                'message': UserRepository.USER_NOT_EXISTS_MESSAGE
            }

    def verify_password(self):
        """
        Verifies password
        """
        password_verified = verify_password(
            plain_password=self.password, hashed_password=self.user_login_info.password
        )
        if not password_verified:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'success': False,
                'message': UserRepository.INCORRECT_PASSWORD_MESSAGE
            }

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_logged_in': True,
                'token': create_jwt_token(data={
                    '__ud': AESCipher.encrypt(data=self.user_login_info.id)
                }),
                'user_data': {
                    'id': self.user_login_info.id,
                    'name': self.user_login_info.name,
                    'email': self.user_login_info.email,
                    'username': self.user_login_info.username
                }
            }
        }

    async def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.verify_user()
        if self.is_send_response:
            return
        self.verify_password()
        if self.is_send_response:
            return
        self.prepare_response()
