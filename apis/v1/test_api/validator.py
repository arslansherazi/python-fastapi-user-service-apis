from pydantic.main import BaseModel


class TestApiValidator(BaseModel):
    name: str
    roll_no: str
