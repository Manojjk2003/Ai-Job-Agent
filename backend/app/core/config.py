from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Career Agent API"
    app_env: str = "development"
    debug: bool = True
    database_url: str
    firebase_credentials_path: str | None = None
    cors_origins: list[str] = ["http://localhost:4200"]
    local_storage_path: str = "./private-storage"
    max_resume_file_size_mb: int = 10
    gemini_api_key: str | None = None
    gemini_model: str | None = None
    max_jd_analysis_chars: int = 20000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
