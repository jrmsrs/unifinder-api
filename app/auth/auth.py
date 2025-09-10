from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from fastapi import Security

from app.infra.config import Settings

security = HTTPBearer(auto_error=False, description="Token Supabase")

signing_key = Settings.signing_key

def get_user_session(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Valida o JWT vindo do Supabase e retorna a sessão do usuário.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            signing_key,
            audience="authenticated",
            algorithms=["HS256"]
        )

        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("user_metadata").get("role"),
            "raw": payload,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{str(e)}",
        ) from Exception


def require_role(required_role: str):
    def dependency(user: dict = Depends(get_user_session)):
        if user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return user
    return dependency