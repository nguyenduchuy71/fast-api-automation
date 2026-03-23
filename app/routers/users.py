from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

# In-memory store for demo purposes
_users: dict[int, dict] = {}
_next_id = 1


@router.get("/", response_model=List[UserResponse])
async def list_users():
    return [UserResponse(id=uid, **data) for uid, data in _users.items()]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    if user_id not in _users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(id=user_id, **_users[user_id])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    global _next_id
    data = user.model_dump(exclude={"password"})
    _users[_next_id] = data
    response = UserResponse(id=_next_id, **data)
    _next_id += 1
    return response


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate):
    if user_id not in _users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    updates = user.model_dump(exclude_none=True)
    _users[user_id].update(updates)
    return UserResponse(id=user_id, **_users[user_id])


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if user_id not in _users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    del _users[user_id]
