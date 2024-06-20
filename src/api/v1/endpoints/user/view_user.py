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


class UserInfo(BaseModel):
    Id: str
    UserName: Optional[str] = None
    NormalizedUserName: Optional[str] = None
    Email: Optional[str] = None
    NormalizedEmail: Optional[str] = None
    EmailConfirmed: Optional[bool] = None
    PhoneNumber: Optional[str] = None
    PhoneNumberConfirmed: Optional[bool] = None
    TwoFactorEnabled: Optional[bool] = None
    LockoutEnd: Optional[str] = None
    LockoutEnabled: Optional[bool] = None
    AccessFailedCount: Optional[int] = None

@router.get("/get_user_info/{user_id}", response_model=UserInfo)
async def get_user_info(user_id: str):
    query = """
            SELECT Id, UserName, NormalizedUserName, Email, NormalizedEmail, EmailConfirmed, 
                PhoneNumber, PhoneNumberConfirmed, TwoFactorEnabled, 
                CONVERT(VARCHAR, LockoutEnd, 126) as LockoutEnd, 
                LockoutEnabled, AccessFailedCount 
            FROM AspNetUsers 
            WHERE Id = ?
            """
    result = retrival_query_user(query, (user_id,))
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_info = result[0]
    
    # Convert datetimeoffset to string
    lockout_end = user_info[9] if user_info[9] else None
    
    return UserInfo(
        Id=user_info[0],
        UserName=user_info[1],
        NormalizedUserName=user_info[2],
        Email=user_info[3],
        NormalizedEmail=user_info[4],
        EmailConfirmed=user_info[5],
        PhoneNumber=user_info[6],
        PhoneNumberConfirmed=user_info[7],
        TwoFactorEnabled=user_info[8],
        LockoutEnd=lockout_end,
        LockoutEnabled=user_info[10],
        AccessFailedCount=user_info[11]
    )


@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: str):
    # Kiểm tra xem người dùng có tồn tại không
    check_query = f"SELECT Id FROM AspNetUsers WHERE Id = '{user_id}'"
    check_result = retrival_query(check_query)
    if not check_result:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Truy vấn SQL để xóa người dùng
    delete_query = f"DELETE FROM AspNetUsers WHERE Id = '{user_id}'"
    execute_query(delete_query)
    return {"message": "User deleted successfully"}

@router.put("/update_user/{user_id}")
async def update_user(user_id: str,
                      user_name: Optional[str] = Form(None),
                      email: Optional[str] = Form(None),
                      phone_number: Optional[str] = Form(None),
                      two_factor_enabled: Optional[bool] = Form(None)):
    # Kiểm tra xem người dùng có tồn tại không
    check_query = f"SELECT Id FROM AspNetUsers WHERE Id = '{user_id}'"
    check_result = retrival_query(check_query)
    if not check_result:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Tạo câu truy vấn cập nhật động
    update_fields = []
    if user_name is not None:
        update_fields.append(f"UserName = '{user_name}'")
        update_fields.append(f"NormalizedUserName = '{user_name.upper()}'")
    if email is not None:
        update_fields.append(f"Email = '{email}'")
        update_fields.append(f"NormalizedEmail = '{email.upper()}'")
    if phone_number is not None:
        update_fields.append(f"PhoneNumber = '{phone_number}'")
    if two_factor_enabled is not None:
        update_fields.append(f"TwoFactorEnabled = {1 if two_factor_enabled else 0}")
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    update_query = f"""
    UPDATE AspNetUsers
    SET {', '.join(update_fields)}
    WHERE Id = '{user_id}'
    """
    execute_query(update_query)
    return {"message": "User updated successfully"}


@router.get("/get_all_users", response_model=List[UserInfo])
async def get_all_users():
    select_query = """
            SELECT Id, UserName, NormalizedUserName, Email, NormalizedEmail, EmailConfirmed, 
                PhoneNumber, PhoneNumberConfirmed, TwoFactorEnabled, 
                CONVERT(VARCHAR, LockoutEnd, 126) as LockoutEnd, 
                LockoutEnabled, AccessFailedCount 
            FROM AspNetUsers
            """
    result = fetch_query_user(select_query)
    if not result:
        raise HTTPException(status_code=404, detail="No users found")
    
    users_info = []
    for user in result:
        users_info.append(UserInfo(
            Id=user['Id'],
            UserName=user['UserName'],
            NormalizedUserName=user['NormalizedUserName'],
            Email=user['Email'],
            NormalizedEmail=user['NormalizedEmail'],
            EmailConfirmed=user['EmailConfirmed'],
            PhoneNumber=user['PhoneNumber'],
            PhoneNumberConfirmed=user['PhoneNumberConfirmed'],
            TwoFactorEnabled=user['TwoFactorEnabled'],
            LockoutEnd=user['LockoutEnd'],
            LockoutEnabled=user['LockoutEnabled'],
            AccessFailedCount=user['AccessFailedCount']
        ))
    
    return users_info