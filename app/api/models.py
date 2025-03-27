from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class ContactModel(BaseModel):
    name: str
    phone: str
    email: str
    message: str

class SettingsModel(BaseSettings):
    PROD: bool = Field(default=True, alias="WILD_WEST_PROD")
