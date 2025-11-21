"""
User service for business logic.
Handles user-related operations and calls the databridge.
"""
from typing import Optional
from datetime import datetime
from models.user import User, UserCreate, UserUpdate, UserResponse
from database.databridge import DataBridge


class UserService:
    """Service layer for user operations"""
    
    def __init__(self, db: DataBridge):
        self.db = db
    
    async def get_all_users(self) -> list[UserResponse]:
        """
        Get all users from the database.
        """
        query = "SELECT id, username, email, full_name, created_at, updated_at FROM users WHERE TRUE ORDER BY created_at DESC"
        rows = await self.db.fetch_all(query)
        
        users = []
        for row in rows:
            user = UserResponse(
                id=row['id'],
                email=row['email'],
                name=row['full_name'] or row['username'],
                role="user",  # Default role, can be updated when role column is added
                is_active=True,  # Default active, can be updated when is_active column is added
                created_at=row['created_at'].isoformat() if row['created_at'] else datetime.now().isoformat()
            )
            users.append(user)
        
        return users
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """
        Get a user by ID.
        For now, returns mock data. Will use database once connected.
        """
        # Mock data
        if user_id == 1:
            return UserResponse(
                id=1,
                email="alice@example.com",
                name="Alice Johnson",
                role="admin",
                is_active=True,
                created_at=datetime.now()
            )
        
        # TODO: Replace with actual database query
        # query = "SELECT * FROM users WHERE id = $1"
        # row = await self.db.fetch_one(query, user_id)
        # return UserResponse(**row) if row else None
        
        return None
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        Create a new user in the database.
        """
        query = """
        INSERT INTO users (username, email, full_name, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id, username, email, full_name, created_at, updated_at
        """
        
        # Use email as username if username not provided
        username = getattr(user_data, 'username', user_data.email.split('@')[0])
        now = datetime.now()
        
        row = await self.db.fetch_one(
            query,
            username,
            user_data.email,
            user_data.name,
            now,
            now
        )
        
        return UserResponse(
            id=row['id'],
            email=row['email'],
            name=row['full_name'] or row['username'],
            role=getattr(user_data, 'role', 'user'),  # Default role
            is_active=True,
            created_at=row['created_at'].isoformat() if row['created_at'] else now.isoformat()
        )
    
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """
        Update a user in the database.
        """
        # Build dynamic update query based on provided fields
        update_fields = []
        values = []
        param_count = 1
        
        if hasattr(user_data, 'name') and user_data.name is not None:
            update_fields.append(f"full_name = ${param_count}")
            values.append(user_data.name)
            param_count += 1
            
        if hasattr(user_data, 'email') and user_data.email is not None:
            update_fields.append(f"email = ${param_count}")
            values.append(user_data.email)
            param_count += 1
        
        if not update_fields:
            # No fields to update, return current user
            return await self.get_user_by_id(user_id)
            
        update_fields.append(f"updated_at = ${param_count}")
        values.append(datetime.now())
        values.append(user_id)  # Add user_id for WHERE clause
        
        query = f"""
        UPDATE users 
        SET {', '.join(update_fields)}
        WHERE id = ${param_count + 1}
        RETURNING id, username, email, full_name, created_at, updated_at
        """
        
        row = await self.db.fetch_one(query, *values)
        
        if not row:
            return None
            
        return UserResponse(
            id=row['id'],
            email=row['email'],
            name=row['full_name'] or row['username'],
            role="user",  # Default role
            is_active=True,  # Default active
            created_at=row['created_at'].isoformat() if row['created_at'] else datetime.now().isoformat()
        )
    
    async def delete_user(self, user_id: int) -> bool:
        """
        Delete a user from the database.
        Note: This is a hard delete. Consider implementing soft delete in production.
        """
        query = "DELETE FROM users WHERE id = $1"
        result = await self.db.execute(query, user_id)
        
        # Check if any rows were affected
        return "DELETE 1" in result

