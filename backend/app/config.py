from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://eduai_user:eduai_pass@postgres:5432/eduai"
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = "eduai-storage"
    R2_ENDPOINT_URL: str = ""
    SECRET_KEY: str = "ganti-dengan-random-string-panjang-minimal-32-karakter"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()