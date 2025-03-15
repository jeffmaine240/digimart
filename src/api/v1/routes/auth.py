from fastapi import APIRouter, Depends, Request, Response, status
from datetime import timedelta
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.api.utils.responses import error_response
from src.api.v1.schemas.response_model import ErrorData
from src.api.v1.schemas.user import UserCreate, UserLogin  
from src.api.db.database import get_db
from src.api.v1.services.user import UserService
from src.api.v1.models import User
from src.api.utils.responses import success_response, error_response


auth_router = APIRouter(
    prefix="/auth", tags=["Authentication"]
)
user_service = UserService()



@auth_router.post("/register")
def register(user_data: UserCreate, db: Session=Depends(get_db)):
    """
    Register a new user
    """
    try:
        email = user_data.email
        existing_user = user_service.get_user_by_email(email, db)
        if existing_user:
            return error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="User with this email already exists",
                data=None,
                status="error"
            )
        user = user_service.create_user(db, user_data)
        print("user:", user)
        access_token = user_service.create_access_token(user.uuid)
        refresh_token = user_service.create_refresh_token(user.uuid)

        response = success_response(
            status_code=status.HTTP_201_CREATED,
            message="User Registered Successfully",
            data = {
                "access_token": access_token,
                "user":
                jsonable_encoder(
                    user, exclude=["password", "is_deleted", "updated_at"])
            },
            status="success"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            expires=timedelta(days=60),
            httponly=True,
            secure=True,
            samesite="none",
        )

        return response
        
    except Exception as e:
        error_data = ErrorData(
            error_type= str(e) or "Unknown error occurred",
            error_details = "Failed to register User"
        )
        return error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="An error occured",
                data=error_data,
                status="error"
            )

    
@auth_router.post("/login")
def login(user_data: UserLogin, db: Session=Depends(get_db)):
    """
    Login a user
    """
    try:
        email = user_data.email
        password = user_data.password
        user = user_service.get_user_by_email(email, db)
        if not user:
            return error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="User with this email does not exist",
                data=None,
                status="error"
            )
        
        if not user_service.verify_password(password, user.password):
            return error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid password",
                data=None,
                status="error"
            )

        access_token = user_service.create_access_token(user.uuid)
        refresh_token = user_service.create_refresh_token(user.uuid)
        response = success_response(
            status_code=status.HTTP_200_OK,
            message="User Logged in Successfully",
            data = {
                "access_token": access_token,
                "user_uuid": user.uuid
            },
            status="success"
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            expires=timedelta(days=60),
            httponly=True,
            secure=True,
            samesite="none",
        )

        return response
        
    except Exception as e:
        error_data = ErrorData(
            error_type= str(e) or "Unknown error occurred",
            error_details = "Failed to login User"
        )
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal Server Error",
            data=error_data,
            status="error"
        )


@auth_router.get("/logout")
def logout(request: Request, response: Response, current_user: User = Depends(user_service.get_current_user)):
    """
    Logout a user
    """
    response.delete_cookie("refresh_token")
    return success_response(
        status_code=status.HTTP_200_OK,
        message="User Logged out Successfully",
        data=None,
        status="success"
    )




