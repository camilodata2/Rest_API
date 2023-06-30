from fastapi.security import HTTPBearer
from starlette.requests import Request
from fastapi.exceptions import HTTPException
import sys
sys.path.append('../venv/jwt_api.py')
import jwt


class JWTBearer(HTTPBearer):
   async def __call__(self, request: Request):
        auth=await super().__call__(request)
        validar_token(auth.credentials)
        if data ['email'] != "juangmail.com":
            raise HTTPException(status_code=403, detail=" credenciales no validas")