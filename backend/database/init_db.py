"""
Database initialization script for the hackathon project.
Creates the necessary tables for users and projects.
"""
import asyncio
from dependencies import get_databridge


async def init_database():
    """Initialize the database with required tables"""
    print("🗄️ Initializing database...")
    
    db = get_databridge()
    
    try:
        await db.connect()
        
        # Create users table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                full_name VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✓ Users table created/verified")
        
        # Create projects table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                status VARCHAR(20) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✓ Projects table created/verified")
        
        # Create indexes for better performance
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_projects_owner ON projects(owner_id);
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
        """)
        print("✓ Database indexes created/verified")
        
        # Insert some sample data (optional)
        existing_users = await db.fetch_val("SELECT COUNT(*) FROM users")
        if existing_users == 0:
            await db.execute("""
                INSERT INTO users (username, email, full_name) VALUES 
                ('john_doe', 'john@example.com', 'John Doe'),
                ('jane_smith', 'jane@example.com', 'Jane Smith')
            """)
            print("✓ Sample users created")
            
            await db.execute("""
                INSERT INTO projects (name, description, owner_id) VALUES 
                ('Machine Learning Pipeline', 'A project to build an ML pipeline for data processing', 1),
                ('Web Dashboard', 'Interactive dashboard for data visualization', 2)
            """)
            print("✓ Sample projects created")
        else:
            print("✓ Database already contains data, skipping sample data insertion")
        
        await db.disconnect()
        print("🎉 Database initialization completed successfully!")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(init_database())