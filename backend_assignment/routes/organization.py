from fastapi import APIRouter, HTTPException, status, Depends, Body
from typing import Dict
from models.organization import OrganizationCreate, OrganizationInDB, OrganizationResponse
from models.admin import AdminInDB
from utils.auth import get_password_hash, get_current_admin
from utils.collection_manager import create_organization_collection, rename_organization_collection, delete_organization_collection
from database import get_database
from bson import ObjectId

router = APIRouter(prefix="/org", tags=["organization"])

@router.post("/create", response_model=OrganizationResponse)
async def create_organization(org_data: OrganizationCreate):
    db = get_database()
    
    # Check if organization already exists
    existing_org = await db.organizations.find_one({"organization_name": org_data.organization_name})
    if existing_org:
        raise HTTPException(status_code=400, detail="Organization name already exists")
    
    # Create dynamic collection
    collection_name = await create_organization_collection(org_data.organization_name)
    
    # Create Organization Document (temporarily without admin_ids)
    org_doc = {
        "organization_name": org_data.organization_name,
        "collection_name": collection_name,
        "connection_details": {}, # In a real scenario, this might point to a specific cluster
        "admin_ids": [] 
    }
    org_result = await db.organizations.insert_one(org_doc)
    org_id = org_result.inserted_id
    
    # Create Admin User
    hashed_password = get_password_hash(org_data.password)
    admin_doc = {
        "email": org_data.email,
        "hashed_password": hashed_password,
        "organization_id": str(org_id)
    }
    admin_result = await db.admins.insert_one(admin_doc)
    admin_id = admin_result.inserted_id
    
    # Update Organization with Admin ID
    await db.organizations.update_one(
        {"_id": org_id},
        {"$push": {"admin_ids": str(admin_id)}}
    )
    
    return OrganizationResponse(
        organization_name=org_data.organization_name,
        organization_id=str(org_id),
        collection_name=collection_name
    )

@router.get("/get", response_model=OrganizationResponse)
async def get_organization(organization_name: str):
    db = get_database()
    org = await db.organizations.find_one({"organization_name": organization_name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    return OrganizationResponse(
        organization_name=org["organization_name"],
        organization_id=str(org["_id"]),
        collection_name=org["collection_name"]
    )

@router.put("/update", response_model=OrganizationResponse)
async def update_organization(
    organization_name: str = Body(..., embed=True),
    email: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    current_admin_payload: dict = Depends(get_current_admin)
):
    db = get_database()
    org_id = current_admin_payload.get("org_id")
    
    current_org = await db.organizations.find_one({"_id": ObjectId(org_id)})
    if not current_org:
        raise HTTPException(status_code=404, detail="Organization not found")
        
    old_name = current_org["organization_name"]
    
    # Rename if needed
    if organization_name != old_name:
        if await db.organizations.find_one({"organization_name": organization_name}):
            raise HTTPException(status_code=400, detail="Organization name already exists")
        
        new_collection = await rename_organization_collection(old_name, organization_name)
        
        await db.organizations.update_one(
            {"_id": ObjectId(org_id)},
            {"$set": {"organization_name": organization_name, "collection_name": new_collection}}
        )
    
    # Update Admin credentials
    admin_id = current_admin_payload.get("admin_id")
    update_data = {}
    if email:
        update_data["email"] = email
    if password:
        update_data["hashed_password"] = get_password_hash(password)
        
    if update_data:
        await db.admins.update_one({"_id": ObjectId(admin_id)}, {"$set": update_data})

    updated_org = await db.organizations.find_one({"_id": ObjectId(org_id)})
    
    return OrganizationResponse(
        organization_name=updated_org["organization_name"],
        organization_id=str(updated_org["_id"]),
        collection_name=updated_org["collection_name"]
    )

@router.delete("/delete")
async def delete_organization(
    organization_name: str,
    current_admin_payload: dict = Depends(get_current_admin)
):
    db = get_database()
    
    org = await db.organizations.find_one({"organization_name": organization_name})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Authorization check
    if current_admin_payload.get("org_id") != str(org["_id"]):
         raise HTTPException(status_code=403, detail="Not authorized to delete this organization")
         
    # Cleanup resources
    await delete_organization_collection(org["collection_name"])
    await db.admins.delete_many({"organization_id": str(org["_id"])})
    await db.organizations.delete_one({"_id": org["_id"]})
    
    return {"detail": f"Organization {organization_name} deleted successfully"}
