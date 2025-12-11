from pydantic import BaseModel, EmailStr, Field, BeforeValidator
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class AdminBase(BaseModel):
    email: EmailStr

class AdminLogin(AdminBase):
    password: str

class AdminInDB(AdminBase):
    admin_id: PyObjectId = Field(..., alias="_id")
    hashed_password: str
    organization_id: str

    class Config:
        populate_by_name = True

class AdminResponse(AdminBase):
    admin_id: str
    organization_id: str
