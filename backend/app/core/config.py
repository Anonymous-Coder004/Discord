from pydantic_settings import BaseSettings

class Settings(BaseSettings): #pydantic model for env variable
    database_hostname:str 
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int
    google_api_key:str
    github_app_id:int
    github_app_private_key:str
    github_repository:str
    huggingfacehub_api_token:str
    class Config:
        env_file=".env"
    
settings=Settings()