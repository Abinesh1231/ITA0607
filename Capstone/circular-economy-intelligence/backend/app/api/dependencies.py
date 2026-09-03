from fastapi import Header, HTTPException
from backend.app.core.security import decode_access_token

def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    return decode_access_token(authorization.split(" ", 1)[1])
