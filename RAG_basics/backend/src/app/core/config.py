from pydantic import SecretStr
from pydantic_settings import BaseSettings , SettingsConfigDict

class settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file =  ".env" ,
        env_file_encoding = "utf-8"
    )
    Secretkey : SecretStr
    Token_Expiration_Time : int = 30
    algorithm : str = "HS256"

setting= settings()


    