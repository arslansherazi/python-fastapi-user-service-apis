SUCCESS_STATUS_CODES = [200, 201]
NOT_FOUND_RESPONSE = {
    404: {
        'success': False,
        'message': '404 Not Found',
        'status_code': 404
    }
}
PNG_IMAGE_EXTENSION = 'png'
PROFILE_IMAGE_FILE_PATH = 'users/{user_id}/images/profile'
FILES_BASE_URL = 'https://picpo-files.s3.us-east-2.amazonaws.com'
USER_SERVICE_DB_NAME = 'spreader_user_service_db'
