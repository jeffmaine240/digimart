from fastapi import File, UploadFile
from sqlalchemy.orm import Session

from models import User, Profile
from utils.responses import error_response, success_response
from services.user import UserService
from api.v1.schemas.profile import UserProfile
from core.security import cloudinary
import cloudinary.uploader


user_service = UserService()

class ProfileService:
    def check_profile_exist_with_user_uuid(self, user_uuid: str, db: Session)-> bool:
        """
        Get profile by user uuid
        """
        profile = db.query(Profile).filter(Profile.user_uuid == user_uuid).first()
        if profile is None:
            return False
        return True
    

    def create_profile(self, db: Session, profile_data: UserProfile, current_user_uuid)-> Profile:
        profile_data_dict = profile_data.model_dump()
        profile = Profile(**profile_data_dict, user_uuid=current_user_uuid)

        db.add(profile)
        db.commit()
        db.refresh(profile)

        return profile


    def update_profile(self, db: Session, profile_data: UserProfile, profile: Profile)-> Profile:
        profile_data_dict = profile_data.model_dump()
        print(profile_data_dict)
        for key, value in profile_data_dict.items():
            if value is not None:
                setattr(profile, key, value) 

        db.add(profile)
        db.commit()
        db.refresh(profile)

        return profile
        
    def upload_avatar(self, db: Session, current_user_uuid: str, avatar_file):
        """
        Upload user avatar
        """
        user_profile = db.query(Profile).filter(Profile.user_uuid == current_user_uuid).first()
        upload_result = cloudinary.uploader.upload(
            avatar_file,
            public_id=user_profile.avatar_id if user_profile.avatar is not None else None,
            overwrite=True,
            folder="avatars"
            )
        print(upload_result)
        avatar_url = upload_result.get("secure_url")
        if user_profile.avatar_id is None:
            public_id = upload_result.get("public_id")
            avatar_id = public_id.split("/")[1]
            user_profile.avatar_id = avatar_id

        user_profile.avatar = avatar_url
        db.commit()
        db.refresh(user_profile)
        return user_profile
