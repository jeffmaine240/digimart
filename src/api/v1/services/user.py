from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import datetime as dt
from sqlalchemy.orm.session import Session
from fastapi import Depends, HTTPException, status
import bcrypt

from src.api.db.database import get_db
from src.api.v1.models import User 
from src.api.v1.schemas.user import UserCreate, UserLogin, TokenData
from src.api.core.config import config



oauth2_scheme = HTTPBearer()

class UserService:

    def hash_password(self, password: str) -> str:
        # Encode the password to bytes
        password_bytes = password.encode("utf-8")
        # Hash the password and Decode the hashed password to a string for storage
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")
        print("password_hash:", password_hash)
        return password_hash
    

    def verify_password(self, password: str, password_hash: str) -> bool:
        # Encode the password and hashed password to bytes
        password_bytes = password.encode("utf-8")
        hashed_password_bytes = password_hash.encode("utf-8")
        # Verify the password
        return bcrypt.checkpw(password_bytes, hashed_password_bytes)
    


    def get_user_by_email(self, email: str, db: Session) -> User:
        user = db.query(User).filter(User.email == email).first()
        return user
    
    def get_user_by_uuid(self, user_uuid: str, db: Session) -> User:
        user = db.query(User).filter(User.uuid == user_uuid).first()
        return user
    
    def get_user_by_sub(self, google_sub: str, db:Session) -> User:
        user = db.query(User).filter(User.google_sub == google_sub).first()
        return user
    

    def create_access_token(self, user_id: str) -> str:
        """Function to create access token"""
        expires = dt.datetime.now(dt.timezone.utc) + dt.timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        data = {"user_id": user_id, "exp": expires, "type": "access"}
        encoded_jwt = jwt.encode(data, config.APP_SECRET, config.JWT_ALGORITHM)
        return encoded_jwt
    

    def create_refresh_token(self, user_id: str) -> str:
        """Function to create access token"""

        expires = dt.datetime.now(
            dt.timezone.utc) + dt.timedelta(days=config.JWT_REFRESH_EXPIRY)
        data = {"user_id": user_id, "exp": expires, "type": "refresh"}
        encoded_jwt = jwt.encode(data, config.APP_SECRET, config.JWT_ALGORITHM)
        return encoded_jwt
    
    def verify_access_token(self, access_token: str, credentials_exception):
        """Function to decode and verify access token"""

        try:
            payload = jwt.decode(access_token,
                                 config.APP_SECRET,
                                 algorithms=[config.JWT_ALGORITHM])
            user_id = payload.get("user_id")
            token_type = payload.get("type")

            if user_id is None:
                raise credentials_exception

            if token_type == "refresh":
                raise HTTPException(detail="Refresh token not allowed",
                                    status_code=400)

            token_data = TokenData(id=user_id)

        except JWTError as err:
            print(err)
            raise credentials_exception

        return token_data


    def create_user(self, db: Session, user_data: UserCreate) -> User:

        user_data_dict = user_data.model_dump(exclude={"password"})
        user = User(**user_data_dict, password=self.hash_password(user_data.password))
        
        #save to database
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def login_user(self, user: User, user_data: UserLogin):
        password_hash = user.password
        password = user_data.password
        if self.verify_password(password, password_hash):
            return True
        return False


    def get_current_user(
        self,
        auth: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
    ) -> User:
        """Function to get current logged in user"""

        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        access_token = auth.credentials

        token = self.verify_access_token(access_token, credentials_exception)
        user = db.query(User).filter(User.uuid == token.id).first()
        if not user:
            raise credentials_exception
        user.update_last_login()

        return user




        


    

    


        