from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class SignUpRequest(BaseModel):
    user_identity: str
    user_email: EmailStr
    user_mobile: str
    user_full_name: str
    user_gender: str
    user_birthday: date
    user_password: str
