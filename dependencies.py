from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from security import oauth2_scheme, SECRET_KEY, ALGORITHM
from database import sessionLocal
from models import User

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = sessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if user is None:
        raise credentials_exception

    return user
