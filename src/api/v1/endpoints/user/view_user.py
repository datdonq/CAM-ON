from fastapi import APIRouter, Depends, Form, UploadFile, File, BackgroundTasks,Query
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from starlette.responses import FileResponse

from database import get_db
from model import *
from auth import *
from passlib.context import CryptContext 
router = APIRouter()
security = HTTPBasic()

pwd_context  = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    db = next(get_db())

    user = db.query(User).filter(User.username == username).first()

    if not user :
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if user and pwd_context.verify(password, user.password):
        access_token_expires = timedelta(minutes=90)
        access_token = create_access_token(data={"username": username}, expires_delta=access_token_expires)
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": access_token, "token_type": "bearer", "username": username  } 

class UserCreate(BaseModel):
    username: str
    password: str
    phone: Optional[int] = None
    email: Optional[str] = None
    
@router.post("/register")
async def register(usercreate:UserCreate):
    db = next(get_db())

    # Kiểm tra xem tên người dùng đã tồn tại chưa
    user = db.query(User).filter(User.username == usercreate.username).first()

    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Mã hóa mật khẩu
    hashed_password = pwd_context.hash(usercreate.password)


    new_user = User(username=usercreate.username,phone=usercreate.phone ,email=usercreate.email, password=hashed_password)
    db.add(new_user)

    db.commit()

    return {"message": "Registration successful"}


class CameraCreate(BaseModel):
    camera_url : str 
@router.get("/add_camera")
async def add_new_camera(current_user : User = Depends(get_current_user)):

    return {"message": "Registration successful"}
    