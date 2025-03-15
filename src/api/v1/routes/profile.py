from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary


from src.api.utils.responses import error_response, success_response
from src.api.v1.models import User
from src.api.v1.schemas.profile import CreateUserProfile
from src.api.db.database import get_db
from src.api.v1.schemas.response_model import ErrorData
from src.api.v1.services.user import UserService
from src.api.v1.services.profile import ProfileService
from src.api.core.config import config

profile_router = APIRouter(
    prefix="/user/profile", tags=["Profile"]
)
user_service = UserService()
profile_service = ProfileService()


@profile_router.post("/create")
def create_profile(profile_data: CreateUserProfile, db: Session=Depends(get_db), current_user: User = Depends(user_service.get_current_user)):
    """
    Create a new user profile
    """
    current_user_uuid = current_user.uuid
    check_profile = profile_service.check_profile_exist_with_user_id(current_user_uuid, db)
    if check_profile:
        return error_response(
            status_code=400,
            message="Profile already exists",
            data=None,
            status="error"
        )

    try:
        profile = profile_service.create_profile(db, profile_data, current_user_uuid)
        return success_response(
            status_code=201,
            message="Profile created successfully",
            data={
                "profile_detail": profile
            },
            status="success")
    
    except Exception as e:
        error_data = ErrorData(
            error_type= str(e) or "Unknown error occurred",
            error_details = "Failed to create profile"
        )
        return error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occurred",
                data=error_data,
                status="error"
            )
    


@profile_router.put("/avatar")
def upload_avatar(avatar: UploadFile = File(...), db: Session=Depends(get_db), current_user: User = Depends(user_service.get_current_user)):
    """
    Upload user profile avatar
    """
    print(avatar.content_type)
    current_user_uuid = current_user.uuid
    check_profile = profile_service.check_profile_exist_with_user_id(current_user_uuid, db)
    if not check_profile:
        return error_response(
            status_code=400,
            message="Profile does not exist",
            data=None,
            status="error"
        )

    if not avatar.content_type.startswith("image/"):
        return error_response(
            status_code=400,
            message="Only image files are allowed",
            data=None,
            status="error"
        )

    MAX_FILE_SIZE = config.MAX_FILE_SIZE * 1024 * 1024  # 5 MB
    if avatar.size > MAX_FILE_SIZE:
        return error_response(
            status_code=400,
            message="Image size must be less than 5 MB",
            data=None,
            status="error"
        )
    try:
        profile_avatar = profile_service.upload_avatar(db, current_user_uuid, avatar.file)
        if profile_avatar is not None:
            return success_response(
                status_code=201,
                message="Avatar uploaded successfully",
                data={
                    "profile_detail": profile_avatar
                },
                status="success")
        
        return error_response(
                status_code=400,
                message="Failed to upload avatar to the cloud",
                data=None,
                status="error"
            )
    except Exception as e:
        error_data = ErrorData(
            error_type= str(e) or "Unknown error occurred",
            error_details = "Failed to upload avatar"
        )
        return error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occurred",
                data=error_data,
                status="error"
            )