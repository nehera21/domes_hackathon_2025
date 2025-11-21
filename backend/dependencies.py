from services.project_service import ProjectService
from services.user_service import UserService
from database.databridge import DataBridge
import asyncpg
from settings import config
from sqlalchemy.ext.asyncio import create_async_engine


async def create_database_connection() -> asyncpg.Connection:
    """Create and return a new database connection using settings from config"""
    database_config = config.database
    return await asyncpg.connect(
        database_config.url,
        min_size=2,
        max_size=10,
        ssl='require',  # Required for Neon
        timeout=3
    )


postgres_engine = create_async_engine(
    "postgresql+asyncpg://",
    async_creator=create_database_connection,
)

_databridge = None
_user_service = None
_project_service = None


def get_databridge() -> DataBridge:
    global _databridge
    if _databridge is None:
        _databridge = DataBridge()
    return _databridge

def get_user_service() -> UserService:
    global _user_service
    if _user_service is None:
        _user_service = UserService(get_databridge())
    return _user_service

def get_project_service() -> ProjectService:
    global _project_service
    if _project_service is None:
        _project_service = ProjectService(get_databridge())
    return _project_service
