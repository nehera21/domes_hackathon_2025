"""
Project API routes.
"""
from typing import List
from dependencies import get_project_service
from fastapi import APIRouter, HTTPException, status, Query, Depends
from models.project import ProjectCreate, ProjectUpdate, ProjectResponse
from services.project_service import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)


@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    owner_id: int = Query(None, description="Filter by owner ID"), 
    service: ProjectService = Depends(get_project_service)
):
    """Get all projects, optionally filtered by owner"""
    if owner_id:
        return await service.get_projects_by_owner(owner_id)
    return await service.get_all_projects()


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int, 
    service: ProjectService = Depends(get_project_service)
):
    """Get a specific project by ID"""
    project = await service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return project


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate, 
    service: ProjectService = Depends(get_project_service)
):
    """Create a new project"""
    return await service.create_project(project_data)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int, 
    project_data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    """Update a project"""
    project = await service.update_project(project_id, project_data)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """Delete a project"""
    success = await service.delete_project(project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return None

