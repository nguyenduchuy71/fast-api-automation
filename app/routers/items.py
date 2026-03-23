from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])

# In-memory store for demo purposes
_items: dict[int, dict] = {}
_next_id = 1


@router.get("/", response_model=List[ItemResponse])
async def list_items():
    return [ItemResponse(id=iid, **data) for iid, data in _items.items()]


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    if item_id not in _items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return ItemResponse(id=item_id, **_items[item_id])


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    global _next_id
    data = item.model_dump()
    _items[_next_id] = data
    response = ItemResponse(id=_next_id, **data)
    _next_id += 1
    return response


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate):
    if item_id not in _items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    updates = item.model_dump(exclude_none=True)
    _items[item_id].update(updates)
    return ItemResponse(id=item_id, **_items[item_id])


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    if item_id not in _items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del _items[item_id]
