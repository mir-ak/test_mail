
from pydantic import BaseModel


class SendEmail(BaseModel):
    email: str


