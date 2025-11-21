"""
Project service for business logic.
Handles project-related operations and calls the databridge.
"""
from typing import Optional
from datetime import datetime
from models.project import Project, ProjectCreate, ProjectUpdate, ProjectResponse


class ProjectService:
    """Service layer for project operations"""

    def __init__(self, db):
        self.db = db
    
    async def get_all_projects(self) -> list[ProjectResponse]:
        """
        Get all projects from the database.
        """
        query = """
        SELECT p.id, p.name, p.description, p.status, p.owner_id, 
               p.created_at, p.updated_at, u.full_name as owner_name
        FROM projects p
        LEFT JOIN users u ON p.owner_id = u.id
        ORDER BY p.created_at DESC
        """
        rows = await self.db.fetch_all(query)
        
        projects = []
        for row in rows:
            project = ProjectResponse(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                status=row['status'],
                owner_id=row['owner_id'],
                owner_name=row['owner_name'] if row['owner_name'] else "Unknown",
                created_at=row['created_at'].isoformat() if row['created_at'] else datetime.now().isoformat(),
                updated_at=row['updated_at'].isoformat() if row['updated_at'] else datetime.now().isoformat()
            )
            projects.append(project)
        
        return projects
    
    async def get_project_by_id(self, project_id: int) -> Optional[ProjectResponse]:
        """
        Get a project by ID from the database.
        """
        query = """
        SELECT p.id, p.name, p.description, p.status, p.owner_id, 
               p.created_at, p.updated_at, u.full_name as owner_name
        FROM projects p
        LEFT JOIN users u ON p.owner_id = u.id
        WHERE p.id = $1
        """
        row = await self.db.fetch_one(query, project_id)
        
        if not row:
            return None
            
        return ProjectResponse(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            status=row['status'],
            owner_id=row['owner_id'],
            owner_name=row['owner_name'] if row['owner_name'] else "Unknown",
            created_at=row['created_at'].isoformat() if row['created_at'] else datetime.now().isoformat(),
            updated_at=row['updated_at'].isoformat() if row['updated_at'] else datetime.now().isoformat()
        )
    
    async def get_projects_by_owner(self, owner_id: int) -> list[ProjectResponse]:
        """
        Get all projects owned by a specific user from the database.
        """
        query = """
        SELECT p.id, p.name, p.description, p.status, p.owner_id, 
               p.created_at, p.updated_at, u.full_name as owner_name
        FROM projects p
        LEFT JOIN users u ON p.owner_id = u.id
        WHERE p.owner_id = $1
        ORDER BY p.created_at DESC
        """
        rows = await self.db.fetch_all(query, owner_id)
        
        projects = []
        for row in rows:
            project = ProjectResponse(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                status=row['status'],
                owner_id=row['owner_id'],
                owner_name=row['owner_name'] if row['owner_name'] else "Unknown",
                created_at=row['created_at'].isoformat() if row['created_at'] else datetime.now().isoformat(),
                updated_at=row['updated_at'].isoformat() if row['updated_at'] else datetime.now().isoformat()
            )
            projects.append(project)
        
        return projects
    
    async def create_project(self, project_data: ProjectCreate) -> ProjectResponse:
        """
        Create a new project in the database.
        """
        query = """
        INSERT INTO projects (name, description, status, owner_id, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id, name, description, status, owner_id, created_at, updated_at
        """
        now = datetime.now()
        row = await self.db.fetch_one(
            query,
            project_data.name,
            project_data.description,
            getattr(project_data, 'status', 'active'),  # Default status
            project_data.owner_id,
            now,
            now
        )
        
        # Get owner name
        owner_query = "SELECT full_name FROM users WHERE id = $1"
        owner_row = await self.db.fetch_one(owner_query, project_data.owner_id)
        owner_name = owner_row['full_name'] if owner_row and owner_row['full_name'] else "Unknown"
        
        return ProjectResponse(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            status=row['status'],
            owner_id=row['owner_id'],
            owner_name=owner_name,
            created_at=row['created_at'].isoformat() if row['created_at'] else now.isoformat(),
            updated_at=row['updated_at'].isoformat() if row['updated_at'] else now.isoformat()
        )
    
    async def update_project(self, project_id: int, project_data: ProjectUpdate) -> Optional[ProjectResponse]:
        """
        Update a project in the database.
        """
        # Build dynamic update query based on provided fields
        update_fields = []
        values = []
        param_count = 1
        
        if hasattr(project_data, 'name') and project_data.name is not None:
            update_fields.append(f"name = ${param_count}")
            values.append(project_data.name)
            param_count += 1
            
        if hasattr(project_data, 'description') and project_data.description is not None:
            update_fields.append(f"description = ${param_count}")
            values.append(project_data.description)
            param_count += 1
            
        if hasattr(project_data, 'status') and project_data.status is not None:
            update_fields.append(f"status = ${param_count}")
            values.append(project_data.status)
            param_count += 1
        
        if not update_fields:
            # No fields to update, return current project
            return await self.get_project_by_id(project_id)
            
        update_fields.append(f"updated_at = ${param_count}")
        values.append(datetime.now())
        values.append(project_id)  # Add project_id for WHERE clause
        
        query = f"""
        UPDATE projects 
        SET {', '.join(update_fields)}
        WHERE id = ${param_count + 1}
        RETURNING id, name, description, status, owner_id, created_at, updated_at
        """
        
        row = await self.db.fetch_one(query, *values)
        
        if not row:
            return None
            
        # Get owner name
        owner_query = "SELECT full_name FROM users WHERE id = $1"
        owner_row = await self.db.fetch_one(owner_query, row['owner_id'])
        owner_name = owner_row['full_name'] if owner_row and owner_row['full_name'] else "Unknown"
        
        return ProjectResponse(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            status=row['status'],
            owner_id=row['owner_id'],
            owner_name=owner_name,
            created_at=row['created_at'].isoformat() if row['created_at'] else datetime.now().isoformat(),
            updated_at=row['updated_at'].isoformat() if row['updated_at'] else datetime.now().isoformat()
        )
    
    async def delete_project(self, project_id: int) -> bool:
        """
        Delete a project from the database.
        """
        query = "DELETE FROM projects WHERE id = $1"
        result = await self.db.execute(query, project_id)
        
        # Check if any rows were affected
        return "DELETE 1" in result

