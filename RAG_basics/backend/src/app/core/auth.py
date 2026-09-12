from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from .config import setting
from datetime import timezone, UTC , timedelta ,datetime
import jwt
password_hash = PasswordHash.recommended()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/users/token"
)

def Password_Hash(password : str) :
    return password_hash.hash(password)


def Verify_Password (plian_password : str , verified_password : str) :
    return password_hash.verify(plian_password,verified_password)


def access_token (data : dict , expiration : timedelta | None = None ) :

    to_encode = data.copy()
    if expiration :
        expiration_time = datetime.now(UTC) + expiration
    else : 
        expiration_time = datetime.now(UTC) + timedelta(minutes=setting.Token_Expiration_Time)

    to_encode.update({"exp" : expiration_time})
    encoded_jwt = jwt.encode(to_encode , setting.Secretkey.get_secret_value() , algorithm=setting.algorithm)

    return encoded_jwt

def verify_token(token:str):
    try:
        payload = jwt.decode(token,setting.Secretkey.get_secret_value(),algorithm = setting.algorithm)
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token has expired")
    