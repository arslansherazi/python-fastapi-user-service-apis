from app import get_settings
from common.common_helpers import CommonHelpers


class UserRepository(object):
    USERNAME_ALREADY_EXIST = 'username already exists'
    EMAIL_EXISTS_IN_SYSTEM_MESSAGE = 'email already registered with us. Please register with some other email'
    USER_NOT_EXISTS_MESSAGE = 'User does not exist in system'
    INCORRECT_PASSWORD_MESSAGE = 'Password is incorrect'

    settings = get_settings()

    @staticmethod
    def upload_profile_image(profile_image, image_name, image_path):
        """
        Uploads profile image

        :param int user_id: user id
        :param profile_image: profile image
        :param str image_name: profile image name
        :param str image_path: profile image path
        """
        image = CommonHelpers.process_image(image=profile_image, is_profile_image=True)
        CommonHelpers.put_s3_object(image, image_name, image_path)
