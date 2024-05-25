import io
import uuid 
import os
import asyncio


from fastapi import APIRouter, Depends, Form, UploadFile, File, BackgroundTasks,Query
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from starlette.responses import FileResponse
from passlib.context import CryptContext 

from src.db.micro_sql import *
from src.api.v1.endpoints.camera.camera_function import *
from src.db.database import get_db
from src.db.model import *
from src.db.auth import *

router = APIRouter()
security = HTTPBasic()

@router.get("/stream")
async def stream_camera(camera_id:str=Query(None, description="Camera ID") ):
    query = f"SELECT IpAddress FROM Cameras WHERE Id = {camera_id}"
    ip_url = retrival_query(query)
    folder_path = os.path.join("./frames", camera_id)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if not ip_url:
        ip_url = 0
    asyncio.create_task(capture_and_save(ip_url, folder_path))
    return StreamingResponse(capture_webcam(ip_url), media_type="multipart/x-mixed-replace; boundary=frame")

@router.post("/add_camera")
async def add_new_camera(camera_url:str=Form(...),
                         camera_name : str = Form(...),
                         user_id : str = Form(...)):
    # Truy vấn SQL để thêm một dòng vào bảng Cameras
    insert_query = f"""
    INSERT INTO Cameras (Name, IpAddress, AccountId)
    VALUES ('{camera_name}', '{camera_url}', '{user_id}')
    """
    execute_query(insert_query)
    return {"message": "Camera added successfully"}