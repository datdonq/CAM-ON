import io
import uuid 
import os
import asyncio


from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks,Query, Form
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from starlette.responses import FileResponse
from passlib.context import CryptContext 
from typing import Optional, Dict

from src.db.micro_sql import *
from src.api.v1.endpoints.camera.camera_function import *
from src.db.database import get_db
from src.db.model import *
from src.db.auth import *

router = APIRouter()
security = HTTPBasic()
# Dictionary to store active camera tasks
camera_tasks: Dict[str, asyncio.Task] = {}

@router.post("/start_cameras_for_all_user")
async def start_cameras_for_user():
    select_query = f"""
    SELECT Id, IpAddress FROM Cameras
    """
    cameras = fetch_query(select_query)
    if not cameras:
        raise HTTPException(status_code=404, detail="No cameras found for the given user ID")
    
    for camera in cameras:
        camera_id, ip_url = camera.values()
        folder_path = os.path.join("./frames", str(camera_id))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        if ip_url:
            task = asyncio.create_task(detect(ip_url, folder_path))
            camera_tasks[camera_id] = task
    print("Start success")
    
    return {"message": "Cameras started successfully for all user"}


@router.get("/stream")
async def stream_camera(camera_id:str=Query(None, description="Camera ID") ):
    try:
        ip_result = retrival_query(f"SELECT IpAddress FROM Cameras WHERE Id = {camera_id}")
        if not ip_result:
            raise HTTPException(status_code=404, detail="Camera not found")

        ip_url = ip_result[0][0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # if int(camera_id) not in list(camera_tasks.keys()):
    #     raise HTTPException(status_code=404, detail="Camera not found or not running")
    
    return StreamingResponse(capture_webcam(ip_url, True), media_type="multipart/x-mixed-replace; boundary=frame")
# @router.get("/stream/{camera_id}")
# async def stream_camera(camera_id:str ):
#     query = f"SELECT IpAddress FROM Cameras WHERE Id = {camera_id}"
#     ip_url = retrival_query(query)[0][0]
#     folder_path = os.path.join("./frames", camera_id)

#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
#     if not ip_url:
#         ip_url = 0
#     asyncio.create_task(capture_and_save(ip_url, folder_path))
#     return StreamingResponse(capture_webcam(ip_url,True), media_type="multipart/x-mixed-replace; boundary=frame"))

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

@router.delete("/delete_camera/{camera_id}")
async def delete_camera(camera_id: int):
    # Truy vấn SQL để xóa một dòng từ bảng Cameras
    delete_query = f"""
    DELETE FROM Cameras WHERE Id = {camera_id}
    """
    execute_query(delete_query)
    return {"message": "Camera deleted successfully"}

@router.put("/update_camera/{camera_id}")
async def update_camera(camera_id: int,
                        camera_url: Optional[str] = Form(None),
                        camera_name: Optional[str] = Form(None),
                        user_id: Optional[str] = Form(None)):
    # Kiểm tra và tạo câu truy vấn SQL để cập nhật các trường được cung cấp
    update_fields = []
    if camera_name is not None:
        update_fields.append(f"Name = '{camera_name}'")
    if camera_url is not None:
        update_fields.append(f"IpAddress = '{camera_url}'")
    if user_id is not None:
        update_fields.append(f"AccountId = '{user_id}'")
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_query = f"""
    UPDATE Cameras
    SET {', '.join(update_fields)}
    WHERE Id = {camera_id}
    """
    execute_query(update_query)
    return {"message": "Camera updated successfully"}

@router.get("/get_camera/{camera_id}")
async def get_camera(camera_id: int):
    select_query = f"""
    SELECT * FROM Cameras WHERE Id = {camera_id}
    """
    camera = fetch_query(select_query)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera

@router.get("/get_cameras_by_user/{user_id}")
async def get_cameras_by_user(user_id: str):
    select_query = f"""
    SELECT * FROM Cameras WHERE AccountId = '{user_id}'
    """
    cameras = fetch_query(select_query)
    if not cameras:
        raise HTTPException(status_code=404, detail="No cameras found for the given user ID")
    return cameras

@router.get("/get_all_cameras")
async def get_all_cameras():
    select_query = "SELECT * FROM Cameras"
    cameras = fetch_query(select_query)
    if not cameras:
        raise HTTPException(status_code=404, detail="No cameras found")
    return cameras
async def startup_event():
    await start_cameras_for_user()