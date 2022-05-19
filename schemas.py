from pydantic import BaseModel


class AnagramSchema(BaseModel):
    first_string: str
    second_string: str


class AnagramResponseSchema(BaseModel):
    is_anagram: bool
    count: int


class DeviceSchema(BaseModel):
    dev_type: str
    number_of_device_types: int

    class Config:
        orm_mode = True
