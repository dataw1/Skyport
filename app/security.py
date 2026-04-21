from passlib.context import CryptContext
import jwt
from fastapi import Request

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "klucz_szyfru"
ALGORITHM = "HS256"

def get_current_user(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        return None
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return None