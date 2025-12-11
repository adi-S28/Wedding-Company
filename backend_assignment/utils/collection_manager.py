from database import db

async def create_organization_collection(org_name: str) -> str:
    collection_name = f"org_{org_name}"
    # Explicitly create collection
    try:
         await db.create_collection(collection_name)
    except Exception:
        pass
    return collection_name

async def delete_organization_collection(collection_name: str):
    await db.drop_collection(collection_name)

async def rename_organization_collection(old_name: str, new_name: str):
     # Handle collection renaming
     old_collection_name = f"org_{old_name}"
     new_collection_name = f"org_{new_name}"
     
     cols = await db.list_collection_names()
     if new_collection_name in cols:
         raise Exception(f"Collection {new_collection_name} already exists")

     if old_collection_name in cols:
         await db[old_collection_name].rename(new_collection_name)
     else:
         await create_organization_collection(new_name)
     
     return new_collection_name
