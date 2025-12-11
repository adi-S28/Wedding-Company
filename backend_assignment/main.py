from fastapi import FastAPI
from routes import organization, admin

app = FastAPI(title="Organization Management Service", version="1.0.0")

app.include_router(organization.router)
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Organization Management Service is running"}
