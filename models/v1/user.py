from datetime import datetime
from operator import or_

from app import get_settings
from common.constants import CONTRIBUTOR_USER_TYPE
from models.db import Base, session
from sqlalchemy import Column, Integer, String, Boolean, DateTime, TIMESTAMP, text

settings = get_settings()


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': settings.user_service_db_name}

    id = Column(Integer, primary_key=True)
    user_type = Column(Integer, nullable=False, default=CONTRIBUTOR_USER_TYPE)
    name = Column(String(255), nullable=False)
    username = Column(String(255), index=True, nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(256), nullable=False)
    profile_image_url = Column(String(256), default=None)
    email_verification_code = Column(Integer, default=None)
    forgot_password_code = Column(Integer, default=None)
    change_email_code = Column(Integer, default=None)
    is_email_verified = Column(Boolean, default=False)
    email_verification_code_expiration = Column(DateTime, default=None)
    forgot_password_code_expiration = Column(DateTime, default=None)
    change_email_code_expiration = Column(DateTime, default=None)
    is_active = Column(Boolean, default=True)
    created_date = Column(TIMESTAMP, nullable=False, default=datetime.now)
    updated_date = Column(
        TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    )

    @classmethod
    def check_username_availability(cls, username):
        """
        Checks either username is available or not

        :param str username: username
        :rtype bool
        """
        query = session.query()
        query = query.with_entities(cls.username)
        query = query.filter(cls.username == username)
        username = query.first()
        if username:
            return False
        return True

    @classmethod
    def check_email_availability(cls, email):
        """
        Checks either email is already registered or not

        :param str email: email
        :rtype bool
        """
        query = session.query()
        query = query.with_entities(cls.email)
        query = query.filter(cls.email == email)
        email = query.first()
        if email:
            return True
        return False

    @classmethod
    def insert_user_into_db(
            cls, user_type, name, username, email, password, profile_image_url, email_verification_code
    ):
        """
        Adds user into the system

        :param Logger logger: logger
        :param int user_type: user type
        :param str name: name
        :param str username: username
        :param str email: email
        :param str password: password
        :param str profile_image_url: profile image url
        :param int email_verification_code: email verification code

        :rtype int
        :returns user id
        """
        user = cls(
            name=name, user_type=user_type, username=username, email=email, password=password,
            profile_image_url=profile_image_url, email_verification_code=email_verification_code
        )
        session.add(user)
        session.commit()
        return user.id

    @classmethod
    def get_login_info(cls, username):
        """
        Gets user login info

        :param str username: username

        :returns user login info
        """
        query = session.query()
        query = query.with_entities(cls.id, cls.username, cls.email, cls.name, cls.password)
        query = query.filter(or_(cls.username == username, cls.email == username))
        return query.first()
