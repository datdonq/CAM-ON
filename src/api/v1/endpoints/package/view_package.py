from fastapi import APIRouter, Depends, Form, UploadFile, File, BackgroundTasks,Query
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from starlette.responses import FileResponse

from src.db.database import get_db
from src.db.model import *
from src.db.auth import *
from src.db.micro_sql import *
from passlib.context import CryptContext 
from typing import List
router = APIRouter()
security = HTTPBasic()

class Package(BaseModel):
    Id: Optional[int]
    Name: str
    MonthValue: int
    Price: float

@router.post("/packages")
async def create_package(name: str = Form(...), month_value: int = Form(...), price: float = Form(...)):
    insert_query = f"""
    INSERT INTO Packages (Name, MonthValue, Price)
    VALUES ('{name}', {month_value}, {price});
    SELECT SCOPE_IDENTITY();
    """
    execute_query(insert_query)
    return {"massage": "Package added successfully"}

@router.get("/packages/{package_id}", response_model=Package)
async def read_package(package_id: int):
    query = f"SELECT Id, Name, MonthValue, Price FROM Packages WHERE Id = {package_id}"
    result = retrival_query(query)
    if not result:
        raise HTTPException(status_code=404, detail="Package not found")
    package_info = result[0]
    return Package(Id=package_info[0], Name=package_info[1], MonthValue=package_info[2], Price=package_info[3])

@router.put("/packages/{package_id}", response_model=Package)
async def update_package(package_id: int, name: Optional[str] = Form(None), month_value: Optional[int] = Form(None), price: Optional[float] = Form(None)):
    update_fields = []
    if name is not None:
        update_fields.append(f"Name = '{name}'")
    if month_value is not None:
        update_fields.append(f"MonthValue = {month_value}")
    if price is not None:
        update_fields.append(f"Price = {price}")

    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_query = f"""
    UPDATE Packages
    SET {', '.join(update_fields)}
    WHERE Id = {package_id}
    """
    execute_query(update_query)
    return await read_package(package_id)

@router.delete("/packages/{package_id}")
async def delete_package(package_id: int):
    delete_query = f"DELETE FROM Packages WHERE Id = {package_id}"
    execute_query(delete_query)
    return {"message": "Package deleted successfully"}

@router.get("/get_package/{package_id}")
async def get_package(package_id: int):
    select_query = f"""
    SELECT * FROM Packages WHERE Id = {package_id}
    """
    package = fetch_query(select_query)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package

@router.get("/get_all_packages")
async def get_all_packages():
    select_query = "SELECT * FROM Packages"
    packages = fetch_query(select_query)
    if not packages:
        raise HTTPException(status_code=404, detail="No packages found")
    return packages