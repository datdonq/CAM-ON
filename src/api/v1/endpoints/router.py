from fastapi import APIRouter

from src.api.v1.endpoints.camera import view_camera
from src.api.v1.endpoints.user import view_user
from src.api.v1.endpoints.package import view_package
router = APIRouter()

# NEW VERSION
router.include_router(router=view_camera.router, prefix="/v1/camera", tags=["Camera"])
router.include_router(router=view_user.router, prefix="/v1/user", tags=["User"])
router.include_router(router=view_package.router, prefix="/v1/package", tags=["Package"])


