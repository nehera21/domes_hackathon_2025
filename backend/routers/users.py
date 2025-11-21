"""
User API routes.
"""
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.user import UserCreate, UserUpdate, UserResponse
from services.user_service import UserService
from dependencies import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("", response_model=List[UserResponse])
async def get_users(
    service: UserService = Depends(get_user_service)
):
    """Get all users"""
    return await service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Get a specific user by ID"""
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """Create a new user"""
    return await service.create_user(user_data)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    user = await service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Delete a user"""
    success = await service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return None

