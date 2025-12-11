from pydantic import BaseModel, Field, EmailStr, BeforeValidator
from typing import Optional, List, Annotated
from threading import Lock

PyObjectId = Annotated[str, BeforeValidator(str)]

class OrganizationBase(BaseModel):
    organization_name: str

class OrganizationCreate(OrganizationBase):
    email: EmailStr
    password: str

class OrganizationInDB(OrganizationBase):
    organization_id: PyObjectId = Field(..., alias="_id")
    collection_name: str
    connection_details: dict = {}
    admin_ids: List[str] = []

    class Config:
        populate_by_name = True

class OrganizationResponse(OrganizationBase):
    organization_id: str
    collection_name: str
