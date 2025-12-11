from fastapi import APIRouter, HTTPException, status, Depends
from models.admin import AdminLogin, AdminInDB
from utils.auth import get_password_hash, verify_password, create_access_token
from database import get_database
from typing import Dict

router = APIRouter()

@router.post("/login", response_model=Dict[str, str])
async def login(admin_login: AdminLogin):
    db = get_database()
    # Find admin by email
    admin = await db.admins.find_one({"email": admin_login.email})
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    admin_in_db = AdminInDB(**admin)
    if not verify_password(admin_login.password, admin_in_db.hashed_password):
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": admin_in_db.email, "admin_id": str(admin_in_db.admin_id), "org_id": admin_in_db.organization_id}
    )
    return {"access_token": access_token, "token_type": "bearer", "organization_id": admin_in_db.organization_id}
