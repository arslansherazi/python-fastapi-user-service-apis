import uuid

from app import get_settings
from common.base_resource import BaseResource
from common.common_helpers import CommonHelpers
from common.constants import AWS_SENDER_EMAIL, UTF_CHARSET, PNG_IMAGE_EXTENSION
from common.utils import get_boto_client, get_password_hash, create_jwt_token
from models.v1.user import User
from repositories.v1.user_repo import UserRepository
from security.aes import AESCipher


class Signup(BaseResource):
    def __init__(self, request, request_args):
        super().__init__(request, request_args)
        self.version = '1'
        self.end_point = 'signup'
        self.profile_image_url = ''
        self.email_verification_code = CommonHelpers.generate_six_digit_random_code()
        self.settings = get_settings()
        self.profile_image_url = ''

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.user_type = self.request_args.get('user_type')
        self.username = self.request_args.get('username')
        self.email = self.request_args.get('email')
        self.password = self.request_args.get('password')
        self.name = self.request_args.get('name')
        self.profile_image = self.request_args.get('profile_image')
        self.image_name = ''
        self.image_path = ''
        self.password = get_password_hash(self.password)

    def check_username_availability(self):
        """
        Checks that either username is available or not
        """
        self.is_username_available = User.check_username_availability(self.username)
        if not self.is_username_available:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': UserRepository.USERNAME_ALREADY_EXIST,
                'is_available': False
            }

    def check_email_availability(self):
        """
        Checks that either email is available or not
        """
        self.is_email_exists_in_system = User.check_email_availability(self.email)
        if self.is_email_exists_in_system:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': UserRepository.EMAIL_EXISTS_IN_SYSTEM_MESSAGE,
                'is_available': False
            }

    def prepare_profile_image_url(self):
        """
        Prepares profile image url
        """
        self.image_name = '{image_id}.{image_extension}'.format(
            image_id=str(uuid.uuid4()), image_extension=PNG_IMAGE_EXTENSION
        )
        self.image_path = UserRepository.settings.profile_image_file_path
        self.profile_image_url = '{base_url}/{image_path}/{image_name}'.format(
            base_url=UserRepository.settings.files_base_url, image_path=self.image_path, image_name=self.image_name
        )

    async def upload_profile_image(self):
        """
        Uploads profile image. It also generates profile image url for database
        """
        UserRepository.upload_profile_image(
            self.profile_image, self.image_name, self.image_path
        )

    async def insert_user_into_db(self):
        """
        Adds user into the system
        """
        self.user_id = User.insert_user_into_db(
            self.user_type, self.name, self.username, self.email, self.password, self.profile_image_url,
            self.email_verification_code
        )

    async def send_email(self):
        """
        Sends email
        """
        boto_client = get_boto_client(service='ses')
        try:
            boto_client.send_email(
                Destination={
                    'ToAddresses': [self.email]
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': UTF_CHARSET,
                            'Data': 'Your email verification code is {verification_code}'.format(
                                verification_code=self.email_verification_code
                            )
                        }
                    },
                    'Subject': {
                        'Charset': UTF_CHARSET,
                        'Data': 'Spreader - Email Verification Code'
                    }
                },
                Source=AWS_SENDER_EMAIL
            )
        except Exception:
            self.logger.exception('Error occured while sending email')

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_signed_up': True,
                'token': create_jwt_token(data={
                    '__ud': AESCipher.encrypt(data=self.user_id)
                }),
                'name': self.name,
                'email': self.email,
                'username': self.username
            }
        }

    async def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.check_username_availability()
        if self.is_send_response:
            return
        self.check_email_availability()
        if self.is_send_response:
            return
        if self.profile_image:
            self.prepare_profile_image_url()
            await self.upload_profile_image()
        await self.insert_user_into_db()
        # await self.send_email()
        self.prepare_response()
