from app import get_settings
from common.base_resource import BaseResource
from common.utils import verify_password, get_password_hash
from models.v1.user import User
from repositories.v1.user_repo import UserRepository
from security.aes import AESCipher


class ChangePassword(BaseResource):
    def __init__(self, request, request_args, user_id):
        super().__init__(request, request_args)
        self.version = '1'
        self.end_point = 'change_password'
        self.user_id = int(AESCipher.decrypt(user_id))
        self.settings = get_settings()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.current_password = self.request_args.get('current_password')
        self.new_password = self.request_args.get('new_password')

    def verify_current_password(self):
        """
        Verifies current password
        """
        hashed_current_password = User.get_user_password(self.user_id)
        if not verify_password(plain_password=self.current_password, hashed_password=hashed_current_password):
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'success': False,
                'message': UserRepository.INCORRECT_CURRENT_PASSWORD_MESSAGE
            }

    def change_password(self):
        """
        Changes user password
        """
        hashed_new_password = get_password_hash(password=self.new_password)
        User.update_password(self.user_id, hashed_new_password)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_password_changed': True
            },
            'message': 'success'
        }

    async def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.verify_current_password()
        if self.is_send_response:
            return
        self.change_password()
        self.prepare_response()
