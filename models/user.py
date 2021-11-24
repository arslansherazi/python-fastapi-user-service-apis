from datetime import datetime

from common.constants import USER_SERVICE_DB_NAME
from models.db import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime, TIMESTAMP, text


class User(db):
    __tablename__ = 'user'
    __table_args__ = {'schema': USER_SERVICE_DB_NAME}

    id = Column(Integer, primary_key=True)
    username = Column(String(255), index=True, nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(256), nullable=False)
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
