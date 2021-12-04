from pydantic.main import BaseModel


class ChangePasswordApiValidator(BaseModel):
    current_password: str
    new_password: str
