from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary


from utils.responses import error_response, success_response
from models import User
from models.profile import Profile
from api.v1.schemas.profile import UserProfile
from db.session import get_db
from api.v1.schemas.response_model import ErrorData
from services.user import UserService
from services.profile import ProfileService
from core.config import config

profile_router = APIRouter(
    prefix="/user/profile", tags=["Profile"]
)
user_service = UserService()
profile_service = ProfileService()


@profile_router.post("/create")
def create_profile(profile_data: UserProfile, db: Session=Depends(get_db), current_user: User = Depends(user_service.get_current_user)):
    """
    Create a new user profile
    """
    current_user_uuid = current_user.uuid
    profile = profile_service.check_profile_exist_with_user_uuid(current_user_uuid, db)
    if profile:
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
    profile = profile_service.check_profile_exist_with_user_uuid(current_user_uuid, db)
    if not profile:
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
    

@profile_router.post("/update/{profile_uuid}")
def update_profile(profile_uuid: str, profile_data: UserProfile, current_user: User=Depends(user_service.get_current_user), db: Session=Depends(get_db)):
    profile = db.query(Profile).filter(Profile.uuid == profile_uuid).first()
    if profile is None:
        return error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Profile does not exist",
            data=None,
            status="error"
        )
    
    if profile.user_uuid != current_user.uuid:
        return error_response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Not Authorized to make change to this profile",
            data=None,
            status="error"
        )
    try:
        profile_update = profile_service.update_profile(db, profile_data, profile)
        return success_response(
            status_code=status.HTTP_202_ACCEPTED,
            message="Profile updated successfully",
            data={
                "profile_detail": profile_update
            },
            status="success")

    except Exception as e:
        error_data = ErrorData(
            error_type= str(e) or "Unknown error occurred",
            error_details = "Failed to update profile"
        )
        return error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occurred",
                data=error_data,
                status="error"
            )
    
@profile_router.get("/me")
def get_user_profile(current_user: User=Depends(user_service.get_current_user), db: Session=Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_uuid == current_user.uuid).first()
    if profile is not None:
        return success_response(
            status_code=status.HTTP_200_OK,
            message="Profile retrieved successfully",
            data={
                "profile_detail": profile
            },
            status="success")
    
    return error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message="There's no profile for this user yet",
            data=None,
            status="error"
        )

