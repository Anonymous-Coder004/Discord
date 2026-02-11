from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field(..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    google_api_key: str = Field(..., alias="GOOGLE_API_KEY")
    github_app_id: int = Field(..., alias="GITHUB_APP_ID")
    github_app_private_key: str = Field(..., alias="GITHUB_APP_PRIVATE_KEY")
    github_repository: str = Field(..., alias="GITHUB_REPOSITORY")
    huggingfacehub_api_token: str = Field(..., alias="HUGGINGFACEHUB_API_TOKEN")
    database_url: str = Field(..., alias="DATABASE_URL")

    model_config = SettingsConfigDict(env_file=".env")

settings=Settings()
