
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from JWTtoken import verify_token


user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')
admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/admin/login')


def get_current_user(token: str = Depends(admin_oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    verify_data = verify_token(token, credentials_exception)
    if verify_data.userType != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized User")
    return verify_data


def get_current_plantUser(token: str = Depends(user_oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    verify_data = verify_token(token, credentials_exception)
    if verify_data.userType != 'user':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized User")
    return verify_data
