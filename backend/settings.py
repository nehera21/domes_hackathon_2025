"""
Configuration settings loaded from environment variables.
This is a singleton pattern to ensure consistent configuration across the app.
"""
from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class PostgressConfig(BaseModel):
    url: str = os.getenv("DATABASE_URL", "")
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", 5432))
    user: str = os.getenv("DB_USER", "user")
    password: str = os.getenv("DB_PASSWORD", "password")
    database: str = os.getenv("DB_NAME", "dbname")

'''
class OpenAIConfig(BaseModel):
    api_key: str
    api_base: str = "https://api.openai.com/v1"
    model_name: str = "gpt-4"


class AnthropicConfig(BaseModel):
    api_key: str
    api_base: str = "https://api.anthropic.com"
    model_name: str = "claude-2"


class LiveKitConfig(BaseModel):
    url: str
    api_key: str
    api_secret: str


class ElevenLabsConfig(BaseModel):
    api_key: str
    api_base: str = "https://api.elevenlabs.io"
'''

class AppConfig(BaseSettings):
    app_name: str = os.getenv("APP_NAME", "Hackathon Backend")
    api_version: str = os.getenv("API_VERSION", "1.0.0")
    
    # Database Configuration (flat structure for backward compatibility)
    database_url: str = os.getenv("DATABASE_URL", "")
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_user: str = os.getenv("DB_USER", "user")
    db_password: str = os.getenv("DB_PASSWORD", "password")
    db_name: str = os.getenv("DB_NAME", "dbname")
    
    @property
    def database(self) -> PostgressConfig:
        return PostgressConfig(
            url=self.database_url,
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name
        )
    
    @property
    def cors_origins_list(self):
        cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
        return [origin.strip() for origin in cors_origins.split(",")]
    
    #openai: OpenAIConfig = OpenAIConfig()
    #anthropic: AnthropicConfig = AnthropicConfig()
    #livekit: LiveKitConfig = LiveKitConfig()
    #elevenlabs: ElevenLabsConfig = ElevenLabsConfig()


@lru_cache()
def get_settings() -> AppConfig:
    """Get the singleton AppConfig instance"""
    return AppConfig()


config = get_settings()
