"""
Simple script to test the database connection to Neon PostgreSQL.
Run this to verify your database connection is working correctly.
"""
import asyncio
from dependencies import get_databridge
from settings import get_settings


async def test_connection():
    """Test the database connection and run a simple query"""
    settings = get_settings()
    print(f"🧪 Testing connection to database...")
    print(f"   Host: {settings.database.host}")
    print(f"   Database: {settings.database.database}")
    print(f"   User: {settings.database.user}")
    
    try:
        db = get_databridge()
        await db.connect()
        
        # Test with a simple query
        result = await db.fetch_val("SELECT version()")
        print(f"✓ Connection successful!")
        print(f"   PostgreSQL Version: {result}")
        
        # Test creating a simple table (optional)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS connection_test (
                id SERIAL PRIMARY KEY,
                test_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✓ Table creation test passed!")
        
        # Insert and read test data
        await db.execute(
            "INSERT INTO connection_test (test_message) VALUES ($1)",
            "Connection test successful!"
        )
        
        test_data = await db.fetch_one(
            "SELECT * FROM connection_test ORDER BY created_at DESC LIMIT 1"
        )
        print(f"✓ Data insertion and retrieval test passed!")
        print(f"   Latest test record: {test_data}")
        
        await db.disconnect()
        print("✓ All database tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print(f"   Make sure your .env file has the correct Neon database credentials")


if __name__ == "__main__":
    asyncio.run(test_connection())