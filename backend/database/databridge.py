"""
Database connection and query interface.
Acts as a bridge between services and the PostgreSQL database.
"""
from typing import Optional, Any
import asyncpg
from contextlib import asynccontextmanager
from settings import get_settings


class DataBridge:
    """
    Handles all database connections and queries.
    Uses asyncpg for async PostgreSQL operations.
    """
    
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.settings = get_settings()
    
    async def connect(self):
        """Initialize database connection pool"""
        if self.pool is None:
            # Try to use DATABASE_URL first (preferred for Neon), fallback to individual components
            if self.settings.database_url:
                self.pool = await asyncpg.create_pool(
                    self.settings.database_url,
                    min_size=2,
                    max_size=10,
                    ssl='require'  # Required for Neon
                )
                print(f"✓ Database pool connected using connection string")
            else:
                self.pool = await asyncpg.create_pool(
                    host=self.settings.db_host,
                    port=self.settings.db_port,
                    database=self.settings.db_name,
                    user=self.settings.db_user,
                    password=self.settings.db_password,
                    min_size=2,
                    max_size=10,
                    ssl='require'  # Required for Neon
                )
                print(f"  Database pool connected to {self.settings.db_host}:{self.settings.db_port}")
    
    async def disconnect(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            self.pool = None
            print("  Database pool disconnected")
    
    @asynccontextmanager
    async def get_connection(self):
        """Get a database connection from the pool"""
        if self.pool is None:
            await self.connect()
        
        async with self.pool.acquire() as connection:
            yield connection
    
    async def execute(self, query: str, *args) -> str:
        """Execute a query that doesn't return data (INSERT, UPDATE, DELETE)"""
        async with self.get_connection() as conn:
            return await conn.execute(query, *args)
    
    async def fetch_one(self, query: str, *args) -> Optional[dict]:
        """Fetch a single row"""
        async with self.get_connection() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None
    
    async def fetch_all(self, query: str, *args) -> list[dict]:
        """Fetch multiple rows"""
        async with self.get_connection() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]
    
    async def fetch_val(self, query: str, *args) -> Any:
        """Fetch a single value"""
        async with self.get_connection() as conn:
            return await conn.fetchval(query, *args)
