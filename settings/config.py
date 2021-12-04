from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    basic_auth_username: str
    basic_auth_password: str
    user_service_db_name: str
    aws_s3_bucket_name: str
    aws_acl_public_read: str
    aws_standard_storage_class: str
    aws_secret_access_key: str
    aws_access_key_id: str
    encryption_disable_key: str
    encryption_key: str
    encryption_salt: str
    encryption_mode: str
    profile_image_file_path: str
    files_base_url: str
    aws_ses_region: str
    secret_key: str
    algorithm: str

    class Config:
        env_file = '.env'
