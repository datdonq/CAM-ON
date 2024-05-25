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
    phone: Optional[str] = None
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

@router.get("/current_user")
async def get_current_user_info(current_user : User = Depends(get_current_user)):
    db = next(get_db())

    # Lấy thông tin của người dùng hiện tại
    user_info = {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "phone": current_user.phone,
        "email": current_user.email
    }

    # Lấy danh sách các camera của người dùng hiện tại
    cameras = db.query(Camera).filter(Camera.user_id == current_user.user_id).all()
    user_cameras = [{
        "camera_id": camera.camera_id,
        "camera_url": camera.camera_url
    } for camera in cameras]

    # Thêm thông tin về các camera của người dùng vào thông tin người dùng
    user_info["cameras"] = user_cameras

    return user_info

@router.put("/update_user")
async def update_user_info(new_info: UserCreate, current_user: User = Depends(get_current_user)):
    db = next(get_db())

    # Lấy thông tin người dùng cần cập nhật từ cơ sở dữ liệu
    user = db.query(User).filter(User.user_id == current_user.user_id).first()
    if user:
            # Kiểm tra trùng lặp username
        if new_info.username:
            username_exists = db.query(User).filter(User.username == new_info.username, User.user_id != current_user.user_id).first()
            if username_exists:
                raise HTTPException(status_code=400, detail="Username already in use")
        # Kiểm tra trùng lặp số điện thoại
        if new_info.phone:
            phone_exists = db.query(User).filter(User.phone == new_info.phone, User.user_id != current_user.user_id).first()
            if phone_exists:
                raise HTTPException(status_code=400, detail="Phone number already in use")

        # Kiểm tra trùng lặp email
        if new_info.email:
            email_exists = db.query(User).filter(User.email == new_info.email, User.user_id != current_user.user_id).first()
            if email_exists:
                raise HTTPException(status_code=400, detail="Email already in use")
    if user:
        # Cập nhật thông tin người dùng nếu có thông tin mới được cung cấp
        if new_info.username:
            user.username = new_info.username
        if new_info.phone:
            user.phone = new_info.phone
        if new_info.email:
            user.email = new_info.email
        if new_info.password:
            # Mã hóa mật khẩu mới nếu có được cung cấp
            hashed_password = pwd_context.hash(new_info.password)
            user.password = hashed_password

        # Lưu thay đổi vào cơ sở dữ liệu
        db.commit()
        return {"message": "User information updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")



    