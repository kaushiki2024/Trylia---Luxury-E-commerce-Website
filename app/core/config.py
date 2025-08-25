from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    app_name: str = "Trylia API"
    environment: str = "development"
    debug: bool = True

    # Database
    database_url: str = "postgresql+psycopg://tr-usr:tr-pass@localhost:5432/trylia"

    # Security
    jwt_secret_key: str = "super-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    # File/media
    media_base_url: str = "https://cdn.example.com/media/"

settings = Settings()
