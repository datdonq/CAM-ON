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

from src.api.v1.endpoints.camera.camera_function import *

router = APIRouter()
security = HTTPBasic()

@router.get("/stream")
async def stream_camera(camera_id:str=Query(None, description="Camera ID"),
                        ip_url: str=Query(None, description="IP Camera URL") ):
    folder_path = os.path.join("./frames", camera_id)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if not ip_url:
        ip_url = 0
    asyncio.create_task(capture_and_save(ip_url, folder_path))
    return StreamingResponse(capture_webcam(ip_url), media_type="multipart/x-mixed-replace; boundary=frame")


