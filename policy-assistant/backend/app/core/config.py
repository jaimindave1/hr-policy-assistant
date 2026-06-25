from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Policy Assistant"
    app_env: str = "local"
    api_prefix: str = "/api"
    #here ... is for required field and validation_alias is for mapping OPENAI_API_KEY to open_api_key
    open_api_key:str = Field(...,validation_alias="OPENAI_API_KEY") 
    supabase_url: str = Field(..., validation_alias="SUPABASE_URL")
    supabase_service_role_key: str = Field(..., validation_alias="SUPABASE_SERVICE_ROLE_KEY")
    supabase_db_url: str = Field(..., validation_alias="SUPABASE_DB_URL")

    upload_dir: Path = Path("uploads")
    max_upload_size_mb: int = 20

    openai_chat_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    retrieval_top_k: int = 5
    relevance_threshold: float = 0.72

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()


